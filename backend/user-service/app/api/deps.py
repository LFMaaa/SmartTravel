from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from common.auth import decode_token

from ..database import get_db
from ..models.user import User
from ..services.auth_service import AuthService

security = HTTPBearer(auto_error=False)


async def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """从 JWT Token 解析当前登录用户"""
    if credentials is None:
        raise HTTPException(status_code=401, detail="未提供认证令牌")

    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="令牌无效或已过期")
    if payload.type != "access":
        raise HTTPException(status_code=401, detail="请使用访问令牌")

    user = await AuthService.get_user_by_id(db, payload.sub)
    if user is None:
        raise HTTPException(status_code=401, detail="用户不存在")

    return user


async def get_optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """可选认证：有 Token 则解析，无 Token 返回 None"""
    if credentials is None:
        return None

    payload = decode_token(credentials.credentials)
    if payload is None or payload.type != "access":
        return None

    return await AuthService.get_user_by_id(db, payload.sub)