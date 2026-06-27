"""
短信服务 — 两种模式:

模式1: 号码认证服务 (dypnsapi，模板 CODE 为纯数字如 100001)
  1. 调用阿里云 SendSmsVerifyCode API，服务端自动生成验证码并发送
  2. API 返回验证码（return_verify_code=True）
  3. 将验证码缓存到 Redis (TTL 5min)

模式2: 普通短信服务 (dysmsapi，模板 CODE 为 SMS_xxxxxxxxx)
  1. 本地生成6位随机验证码
  2. 调用阿里云 SendSms API 发送到用户手机
  3. 将验证码缓存到 Redis

验证: 从 Redis/MySQL 读取比对，一致且未过期则通过

配置:
  ALIBABA_CLOUD_ACCESS_KEY_ID     — 阿里云 AccessKey ID
  ALIBABA_CLOUD_ACCESS_KEY_SECRET — 阿里云 AccessKey Secret
  SMS_SIGN_NAME                   — 短信签名名称（号码认证服务 → 签名配置）
  SMS_TEMPLATE_CODE               — 模板 Code（号码认证服务 → 模板配置，如 100001）
  REDIS_URL                       — Redis 连接地址
"""
import asyncio
import os
import logging
import random
from datetime import datetime, timedelta
from functools import partial

import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

SMS_CODE_EXPIRE_SECONDS = 300  # 5分钟
SMS_REDIS_PREFIX = "sms:code:"


class SmsService:
    """短信服务 — Redis 优先缓存 + 阿里云 SMS 发送 + MySQL 回退"""

    @staticmethod
    def _is_dypnsapi() -> bool:
        """判断是否使用号码认证服务（模板 CODE 为纯数字）"""
        tc = os.getenv("SMS_TEMPLATE_CODE", "").strip()
        return tc.isdigit() and len(tc) > 0

    # ==================== 发送 ====================

    @staticmethod
    async def send_code(phone: str, redis: aioredis.Redis | None = None) -> dict:
        """发送验证码并缓存到 Redis，返回 {"code": "123456", "dev_mode": bool}

        号码认证服务: 服务端自动生成验证码，从 API 响应中获取
        普通短信服务: 本地生成验证码
        dev_mode=True 表示未真正发送（权限不足/未配置），前端可展示验证码
        """
        # 1. 发送短信
        response = await SmsService._send_via_aliyun(phone)
        dev_mode = response.get("dev_mode", False)

        # 2. 从响应中提取验证码
        if SmsService._is_dypnsapi():
            code = response.get("verify_code") or response.get("code", "")
            if not code:
                raise RuntimeError("号码认证服务未返回验证码，请检查配置")
        else:
            code = response.get("code", "")

        # 3. 缓存到 Redis
        if redis and code:
            try:
                await redis.setex(
                    f"{SMS_REDIS_PREFIX}{phone}",
                    SMS_CODE_EXPIRE_SECONDS,
                    code,
                )
                logger.info(f"[SMS] 验证码已缓存到 Redis: {phone}")
            except Exception as exc:
                logger.warning(f"[SMS] Redis 缓存失败: {exc}")

        return {"code": code, "dev_mode": dev_mode}

    # ==================== 验证 ====================

    @staticmethod
    async def verify_code(
        phone: str,
        code: str,
        redis: aioredis.Redis | None = None,
        mysql_code: str | None = None,
        mysql_expires_at: datetime | None = None,
    ) -> bool:
        """验证短信验证码 — Redis 优先 → MySQL 回退

        Returns:
            True 验证通过，False 验证失败
        """
        # 1. Redis 优先
        if redis:
            try:
                cached = await redis.get(f"{SMS_REDIS_PREFIX}{phone}")
                if cached is not None:
                    # decode_responses=True 时 Redis 直接返回 str；兼容 bytes 模式
                    cached_str = cached.decode("utf-8") if isinstance(cached, bytes) else str(cached)
                    if cached_str == code:
                        await redis.delete(f"{SMS_REDIS_PREFIX}{phone}")
                        logger.info(f"[SMS] Redis 验证通过: {phone}")
                        return True
                    else:
                        logger.info(f"[SMS] Redis 验证码不匹配: {phone}")
                        return False
            except Exception as exc:
                logger.warning(f"[SMS] Redis 读取失败，回退 MySQL: {exc}")

        # 2. MySQL 回退
        if mysql_code and mysql_expires_at:
            if datetime.utcnow() > mysql_expires_at:
                return False  # 过期
            if mysql_code == code:
                return True
        return False

    # ==================== 阿里云发送 ====================

    @staticmethod
    def _do_send_sms(phone: str, access_key: str, access_secret: str,
                     sign_name: str, template_code: str, code: str = ""):
        """同步发送短信（在线程池中调用，避免阻塞事件循环）

        支持两种模板格式：
        - 纯数字 (如 100001): 号码认证服务 (dypnsapi)，服务端自动生成验证码
        - SMS_xxxxxxxxx: 普通短信服务 (dysmsapi)，需传入本地生成的验证码

        Returns:
            dict: {"verify_code": "123456"} 号码认证服务
                  {"code": "123456"} 普通短信服务
        """
        from alibabacloud_tea_openapi import models as open_api_models

        is_dypnsapi = template_code.isdigit()

        config = open_api_models.Config(
            access_key_id=access_key,
            access_key_secret=access_secret,
        )

        if is_dypnsapi:
            # 号码认证服务 (dypnsapi) — 服务端自动生成验证码
            from alibabacloud_dypnsapi20170525.client import Client as DypnsapiClient
            from alibabacloud_dypnsapi20170525 import models as dypnsapi_models

            config.endpoint = "dypnsapi.aliyuncs.com"
            client = DypnsapiClient(config)

            request = dypnsapi_models.SendSmsVerifyCodeRequest(
                phone_number=phone,
                sign_name=sign_name,
                template_code=template_code,
                template_param='{"code":"##code##","min":"5"}',  # 模板变量：code由服务端生成，min=5分钟
                code_type=1,  # 纯数字验证码
                return_verify_code=True,  # 让 API 返回生成的验证码
            )
            response = client.send_sms_verify_code(request)

            if response.body.code != "OK":
                raise RuntimeError(
                    f"号码认证服务发送失败: {response.body.message}（错误码: {response.body.code}）"
                )

            return {
                "verify_code": str(response.body.model.verify_code),
            }
        else:
            # 普通短信服务 (dysmsapi) — 使用本地生成的验证码
            from alibabacloud_dysmsapi20170525.client import Client as DysmsapiClient
            from alibabacloud_dysmsapi20170525 import models as dysmsapi_models

            config.endpoint = "dysmsapi.aliyuncs.com"
            client = DysmsapiClient(config)

            request = dysmsapi_models.SendSmsRequest(
                phone_numbers=phone,
                sign_name=sign_name,
                template_code=template_code,
                template_param=f'{{"code":"{code}"}}',
            )
            response = client.send_sms(request)

            if response.body.code != "OK":
                raise RuntimeError(
                    f"短信服务发送失败: {response.body.message}（错误码: {response.body.code}）"
                )

            return {"code": code}

    @staticmethod
    async def _send_via_aliyun(phone: str, code: str = ""):
        """异步包装阿里云短信发送，返回包含验证码的 dict"""
        access_key = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID", "").strip()
        access_secret = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "").strip()
        sign_name = os.getenv("SMS_SIGN_NAME", "").strip()
        template_code = os.getenv("SMS_TEMPLATE_CODE", "").strip()

        if not (access_key and access_secret and sign_name and template_code):
            missing = []
            if not access_key: missing.append("ALIBABA_CLOUD_ACCESS_KEY_ID")
            if not access_secret: missing.append("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
            if not sign_name: missing.append("SMS_SIGN_NAME")
            if not template_code: missing.append("SMS_TEMPLATE_CODE")
            logger.warning(
                f"[SMS] 以下配置缺失，走日志模式: {', '.join(missing)}。"
                f"手机号: {phone}"
            )
            if not code:
                code = str(random.randint(100000, 999999))
            logger.warning(f"[SMS] 开发模式验证码: {code}")
            return {"code": code, "dev_mode": True}

        try:
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                partial(
                    SmsService._do_send_sms,
                    phone, access_key, access_secret, sign_name, template_code, code,
                )
            )
            logger.info(f"[SMS] 阿里云发送成功: {phone}")
            return result

        except ImportError:
            logger.error("[SMS] 缺少依赖包，请检查 requirements.txt")
            raise RuntimeError("短信服务依赖包未安装，请联系管理员")
        except RuntimeError as exc:
            msg = str(exc)
            # 权限不足或配置错误 → 自动回退到开发模式
            if "NoPermission" in msg or "Forbidden" in msg or "not authorized" in msg.lower():
                logger.warning(
                    f"[SMS] 阿里云 RAM 权限不足，回退到开发模式。"
                    f"请在 RAM 控制台为子账号添加 dypns:SendSmsVerifyCode 或 dysms:SendSms 权限。"
                    f"手机号: {phone}"
                )
                if not code:
                    code = str(random.randint(100000, 999999))
                logger.warning(f"[SMS] 开发模式验证码: {code}")
                return {"code": code, "dev_mode": True}
            raise
        except Exception as exc:
            msg = str(exc)
            if "NoPermission" in msg or "Forbidden" in msg or "not authorized" in msg.lower():
                logger.warning(
                    f"[SMS] 阿里云 RAM 权限不足，回退到开发模式。手机号: {phone}"
                )
                if not code:
                    code = str(random.randint(100000, 999999))
                logger.warning(f"[SMS] 开发模式验证码: {code}")
                return {"code": code, "dev_mode": True}
            logger.error(f"[SMS] 阿里云调用异常: {exc}，手机号: {phone}")
            raise RuntimeError(f"短信发送异常: {exc}")
