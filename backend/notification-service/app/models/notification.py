from typing import Optional

from sqlalchemy import String, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from common.models import Base, TimestampMixin


class Notification(Base, TimestampMixin):
    """通知消息表 — 对应 init_db.sql §10 notifications"""
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type: Mapped[str] = mapped_column(
        Enum("replan_alert", "payment_reminder", "schedule_reminder", "system", name="notification_type"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[Optional[str]] = mapped_column(JSON, nullable=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    resource_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    resource_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
