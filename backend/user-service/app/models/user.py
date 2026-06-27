from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models import Base, TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    nickname: Mapped[str] = mapped_column(String(50), default="")
    phone: Mapped[Optional[str]] = mapped_column(String(20), unique=True, nullable=True)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    oauth_provider: Mapped[Optional[str]] = mapped_column(String(20), nullable=True, comment="wechat / alipay")
    oauth_openid: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    oauth_unionid: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Password auth
    hashed_password: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    salt: Mapped[Optional[str]] = mapped_column(String(32), nullable=True)

    # SMS verification code
    sms_code: Mapped[Optional[str]] = mapped_column(String(6), nullable=True)
    sms_code_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Pro 会员
    is_pro: Mapped[bool] = mapped_column(default=False, comment="是否为Pro会员")
    pro_expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="Pro会员过期时间")

    # Relations
    preferences: Mapped[Optional["UserPreference"]] = relationship(
        "UserPreference", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class UserPreference(Base, TimestampMixin):
    __tablename__ = "user_preferences"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    travel_style: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="JSON: pace/type/companion")
    budget_range: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="JSON: min/max/per_day")
    constraints: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="JSON: no_climbing/max_walk_steps")
    favorite_destinations: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, comment="JSON array")

    user: Mapped["User"] = relationship("User", back_populates="preferences")
