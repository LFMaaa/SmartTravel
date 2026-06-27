import os
from datetime import datetime, timedelta
from typing import Optional

import jwt
from pydantic import BaseModel


class TokenPayload(BaseModel):
    sub: str          # user_id
    exp: datetime
    iat: datetime
    type: str = "access"  # access / refresh


SECRET_KEY = os.getenv("JWT_SECRET_KEY", "smarttravel-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(user_id: str) -> str:
    payload = TokenPayload(
        sub=user_id,
        exp=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        iat=datetime.utcnow(),
        type="access",
    )
    return jwt.encode(payload.model_dump(), SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    payload = TokenPayload(
        sub=user_id,
        exp=datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
        iat=datetime.utcnow(),
        type="refresh",
    )
    return jwt.encode(payload.model_dump(), SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None