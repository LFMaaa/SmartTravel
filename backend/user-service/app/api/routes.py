from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from common.auth import create_access_token, create_refresh_token, decode_token
from common.schemas import APIResponse

from ..database import get_db, get_redis
from ..services.auth_service import AuthService
from .deps import get_current_user
from ..models.user import User

router = APIRouter()


# ==================== 请求/响应模型 ====================

class RegisterRequest(BaseModel):
    phone: str
    password: str
    sms_code: str
    nickname: str = ""


class LoginRequest(BaseModel):
    phone: str
    password: str


class SmsSendRequest(BaseModel):
    phone: str


class SmsLoginRequest(BaseModel):
    phone: str
    code: str


class WechatLoginRequest(BaseModel):
    code: str
    nickname: str = ""
    avatar_url: str = ""


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class RegisterResponse(BaseModel):
    phone: str
    message: str = "注册成功，请登录"


class UserInfoResponse(BaseModel):
    id: str
    phone: str | None = None
    nickname: str
    avatar_url: str | None = None
    oauth_provider: str | None = None
    is_pro: bool = False
    pro_expire_at: str | None = None
    created_at: str | None = None


# ==================== 密码注册/登录 ====================

@router.post("/register", response_model=APIResponse[RegisterResponse])
async def register(
    req: RegisterRequest,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    """手机号+密码注册 — 短信验证码校验通过后创建账号"""
    user = await AuthService.register(
        db, req.phone, req.password, req.sms_code, redis, req.nickname
    )
    return APIResponse(
        data=RegisterResponse(phone=user.phone, message="注册成功，请登录")
    )


@router.post("/login", response_model=APIResponse[TokenResponse])
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    """手机号+密码登录"""
    user = await AuthService.login(db, req.phone, req.password)
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return APIResponse(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token)
    )


# ==================== 短信验证码 ====================

@router.post("/sms/send", response_model=APIResponse)
async def send_sms_code(
    req: SmsSendRequest,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    """发送短信验证码 — 阿里云 SMS → Redis 缓存 → MySQL 兜底"""
    from fastapi import HTTPException
    try:
        result = await AuthService.send_sms_code(db, req.phone, redis)
    except HTTPException:
        raise
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))
    return APIResponse(data=result, message="验证码已发送")


@router.post("/sms/login", response_model=APIResponse[TokenResponse])
async def login_by_sms(
    req: SmsLoginRequest,
    db: AsyncSession = Depends(get_db),
    redis=Depends(get_redis),
):
    """短信验证码登录 — Redis 优先验证 → MySQL 回退，新用户自动创建"""
    user = await AuthService.login_by_sms(db, req.phone, req.code, redis)
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return APIResponse(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token)
    )


# ==================== 微信登录 ====================

@router.post("/wechat/login", response_model=APIResponse[TokenResponse])
async def login_by_wechat(req: WechatLoginRequest, db: AsyncSession = Depends(get_db)):
    """微信授权登录"""
    user = await AuthService.wechat_login(db, req.code, req.nickname, req.avatar_url)
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return APIResponse(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token)
    )


# ==================== Token 管理 ====================

@router.post("/refresh", response_model=APIResponse[TokenResponse])
async def refresh_token(req: RefreshRequest):
    """刷新 Token"""
    payload = decode_token(req.refresh_token)
    if not payload or payload.type != "refresh":
        from fastapi import HTTPException
        raise HTTPException(status_code=401, detail="无效的刷新令牌")
    access_token = create_access_token(payload.sub)
    refresh_token = create_refresh_token(payload.sub)
    return APIResponse(
        data=TokenResponse(access_token=access_token, refresh_token=refresh_token)
    )


@router.get("/me", response_model=APIResponse[UserInfoResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return APIResponse(
        data=UserInfoResponse(
            id=current_user.id,
            phone=current_user.phone,
            nickname=current_user.nickname,
            avatar_url=current_user.avatar_url,
            oauth_provider=current_user.oauth_provider,
            is_pro=current_user.is_pro,
            pro_expire_at=current_user.pro_expire_at.isoformat() if current_user.pro_expire_at else None,
            created_at=current_user.created_at.isoformat() if current_user.created_at else None,
        )
    )


# ==================== 会员升级 ====================

class UpgradeMemberRequest(BaseModel):
    user_id: str


@router.post("/upgrade-member", response_model=APIResponse)
async def upgrade_member(
    req: UpgradeMemberRequest,
    db: AsyncSession = Depends(get_db),
):
    """升级用户为 Pro 会员（由支付回调调用）"""
    from datetime import datetime, timedelta
    from sqlalchemy import select
    from fastapi import HTTPException

    result = await db.execute(select(User).where(User.id == req.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    user.is_pro = True
    user.pro_expire_at = datetime.utcnow() + timedelta(days=365)
    await db.flush()

    return APIResponse(
        data={"is_pro": True, "pro_expire_at": user.pro_expire_at.isoformat()},
        message="已升级为 Pro 会员",
    )
