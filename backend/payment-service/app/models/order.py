import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Enum, DECIMAL, Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models import Base, TimestampMixin


class Order(Base, TimestampMixin):
    """订单主表 — 对应 init_db.sql §7 orders"""
    __tablename__ = "orders"

    user_id: Mapped[str] = mapped_column(String(36), nullable=False, comment="关联 users 表（同库不同服务，无 FK 约束）")
    itinerary_id: Mapped[Optional[str]] = mapped_column(String(36), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "paid", "timeout", "cancelled", "refunded", name="order_status"),
        default="pending",
    )
    payment_status: Mapped[str] = mapped_column(
        Enum("unpaid", "paid", "refunding", "refunded", name="payment_status"),
        default="unpaid",
    )
    total_amount: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False, default=0)
    delay_token: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="延迟支付 Token（Redis Key）")
    expire_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, comment="延迟支付过期时间")
    paid_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # 关联
    items: Mapped[list["OrderItem"]] = relationship(
        "OrderItem", back_populates="order", cascade="all, delete-orphan", lazy="selectin"
    )


class OrderItem(Base, TimestampMixin):
    """订单项表 — 对应 init_db.sql §8 order_items"""
    __tablename__ = "order_items"

    order_id: Mapped[str] = mapped_column(String(36), ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    resource_type: Mapped[str] = mapped_column(
        Enum("hotel", "ticket", "flight", "restaurant", "insurance", name="resource_type"),
        nullable=False,
    )
    resource_id: Mapped[str] = mapped_column(String(100), nullable=False)
    resource_name: Mapped[str] = mapped_column(String(200), nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    booking_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    check_in: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    check_out: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # 关联
    order: Mapped["Order"] = relationship("Order", back_populates="items")
