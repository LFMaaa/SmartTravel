import hashlib
import os
import logging
from datetime import datetime, timedelta

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User, UserPreference
from .sms_service import SmsService, SMS_CODE_EXPIRE_SECONDS

logger = logging.getLogger(__name__)


class AuthService:
    """认证服务 — 支持密码/短信/微信登录"""

    # ==================== 密码注册/登录 ====================

    @staticmethod
    async def register(
        db: AsyncSession, phone: str, password: str, nickname: str = "",
    ) -> User:
        """手机号+密码注册 — 仅校验手机号和密码，不需要短信验证码"""
        # 1. 检查手机号是否已注册
        result = await db.execute(select(User).where(User.phone == phone))
        existing = result.scalar_one_or_none()
        if existing:
            if existing.hashed_password:
                raise HTTPException(status_code=409, detail="手机号已注册")
            user = existing
        else:
            user = User(phone=phone, nickname=nickname or f"用户{phone[-4:]}")
            db.add(user)
            await db.flush()
            pref = UserPreference(user_id=user.id)
            db.add(pref)

        # 2. 设置密码
        salt = os.urandom(16).hex()
        user.hashed_password = AuthService._hash_password(password, salt)
        user.salt = salt
        if not user.nickname or user.nickname.startswith("用户"):
            user.nickname = nickname or f"用户{phone[-4:]}"
        user.last_login_at = datetime.utcnow()
        return user

    @staticmethod
    async def login(db: AsyncSession, phone: str, password: str) -> User:
        """手机号+密码登录"""
        result = await db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="手机号或密码错误")
        if not user.hashed_password or not user.salt:
            raise HTTPException(status_code=401, detail="该账号未设置密码，请使用短信或微信登录")

        hashed = AuthService._hash_password(password, user.salt)
        if hashed != user.hashed_password:
            raise HTTPException(status_code=401, detail="手机号或密码错误")

        user.last_login_at = datetime.utcnow()
        return user

    # ==================== 短信验证码 ====================

    @staticmethod
    async def send_sms_code(db: AsyncSession, phone: str, redis=None) -> dict:
        """标准流程：生成验证码 → 阿里云发送 → Redis 缓存 → MySQL 兜底"""
        import re
        # 手机号格式校验
        if not re.match(r"^1[3-9]\d{9}$", phone):
            raise HTTPException(status_code=400, detail="手机号格式不正确")

        result = await SmsService.send_code(phone, redis=redis)
        code = result["code"]
        dev_mode = result.get("dev_mode", False)

        # MySQL 兜底：同步写入（Redis 不可用时仍然能验证）
        result_db = await db.execute(select(User).where(User.phone == phone))
        user = result_db.scalar_one_or_none()
        if not user:
            user = User(phone=phone, nickname=f"用户{phone[-4:]}")
            db.add(user)
            await db.flush()
            pref = UserPreference(user_id=user.id)
            db.add(pref)

        user.sms_code = code
        user.sms_code_expires_at = datetime.utcnow() + timedelta(seconds=SMS_CODE_EXPIRE_SECONDS)

        # 只要 sms_service 返回了验证码（开发模式/AK未配/权限回退），就透传给前端
        return {
            "phone": phone,
            "expires_in": SMS_CODE_EXPIRE_SECONDS,
            **({"code": code, "dev_mode": True} if dev_mode else {}),
        }

    @staticmethod
    async def login_by_sms(db: AsyncSession, phone: str, code: str, redis=None) -> User:
        """短信验证码登录 — 自动创建新用户（标准流程：Redis 优先验证 → MySQL 回退）"""
        # 验证验证码
        result = await db.execute(select(User).where(User.phone == phone))
        user = result.scalar_one_or_none()

        if not user:
            # 新用户：自动创建
            user = User(phone=phone, nickname=f"用户{phone[-4:]}")
            db.add(user)
            await db.flush()
            pref = UserPreference(user_id=user.id)
            db.add(pref)
            # 新用户也需要有验证码才能验证通过
            user.sms_code = None
            user.sms_code_expires_at = None

        await AuthService._verify_sms_code_hybrid(user, code, redis)
        user.last_login_at = datetime.utcnow()
        return user

    # ==================== 微信登录 ====================

    @staticmethod
    async def wechat_login(
        db: AsyncSession, code: str, nickname: str = "", avatar_url: str = ""
    ) -> User:
        openid = AuthService._mock_wechat_openid(code)
        return await AuthService.get_or_create_oauth_user(
            db=db, provider="wechat", openid=openid,
            nickname=nickname or f"微信用户{openid[-4:]}", avatar_url=avatar_url,
        )

    @staticmethod
    async def get_or_create_oauth_user(
        db: AsyncSession, provider: str, openid: str,
        nickname: str = "", avatar_url: str = "",
    ) -> User:
        result = await db.execute(
            select(User).where(
                User.oauth_provider == provider, User.oauth_openid == openid,
            )
        )
        user = result.scalar_one_or_none()
        if user:
            user.last_login_at = datetime.utcnow()
            if avatar_url:
                user.avatar_url = avatar_url
            return user

        user = User(
            oauth_provider=provider, oauth_openid=openid,
            nickname=nickname or f"用户{openid[-4:]}",
            avatar_url=avatar_url or None,
            last_login_at=datetime.utcnow(),
        )
        db.add(user)
        await db.flush()
        pref = UserPreference(user_id=user.id)
        db.add(pref)
        return user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> User | None:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    # ==================== 内部 ====================

    @staticmethod
    async def _verify_sms_code_hybrid(user: User, code: str, redis=None) -> bool:
        """混合验证：Redis 优先 → MySQL 回退"""
        # 1. Redis 优先
        if redis:
            verified = await SmsService.verify_code(
                phone=user.phone or "",
                code=code,
                redis=redis,
            )
            if verified:
                # 同步清除 MySQL 中的验证码
                user.sms_code = None
                user.sms_code_expires_at = None
                return True

        # 2. MySQL 回退
        if not user.sms_code or not user.sms_code_expires_at:
            raise HTTPException(status_code=401, detail="请先获取验证码")
        if datetime.utcnow() > user.sms_code_expires_at:
            raise HTTPException(status_code=401, detail="验证码已过期，请重新获取")
        if user.sms_code != code:
            raise HTTPException(status_code=401, detail="验证码错误")

        user.sms_code = None
        user.sms_code_expires_at = None
        return True

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        return hashlib.sha256(f"{password}{salt}".encode()).hexdigest()

    @staticmethod
    def _mock_wechat_openid(code: str) -> str:
        return f"wx_dev_{hashlib.md5(code.encode()).hexdigest()[:16]}"
