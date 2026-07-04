import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import String, Integer, Float, Date, DateTime, Text, ForeignKey, Enum, DECIMAL, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from common.models import Base, TimestampMixin


class Itinerary(Base, TimestampMixin):
    """行程主表 — 对应 init_db.sql §3 itineraries"""
    __tablename__ = "itineraries"

    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title: Mapped[str] = mapped_column(String(200), nullable=False, default="未命名行程")
    destination: Mapped[str] = mapped_column(String(100), nullable=False, comment="主要目的地城市")
    start_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    days: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    total_budget: Mapped[Optional[Decimal]] = mapped_column(DECIMAL(10, 2), nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("draft", "planned", "in_progress", "completed", "cancelled", name="itinerary_status"),
        default="draft",
    )
    source: Mapped[str] = mapped_column(
        Enum("ai_generated", "manual", "cloned", "replanned", name="itinerary_source"),
        default="ai_generated",
    )
    dify_workflow_run_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    raw_input: Mapped[Optional[str]] = mapped_column(JSON, nullable=True, comment="用户原始自然语言输入")

    # 关联
    days_list: Mapped[list["ItineraryDay"]] = relationship(
        "ItineraryDay", back_populates="itinerary", cascade="all, delete-orphan",
        order_by="ItineraryDay.day_number",
    )
    versions: Mapped[list["ItineraryVersion"]] = relationship(
        "ItineraryVersion", back_populates="itinerary", cascade="all, delete-orphan",
    )


class ItineraryDay(Base, TimestampMixin):
    """行程日表 — 对应 init_db.sql §4 itinerary_days"""
    __tablename__ = "itinerary_days"

    itinerary_id: Mapped[str] = mapped_column(String(36), ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    day_number: Mapped[int] = mapped_column(Integer, nullable=False)
    date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    weather: Mapped[Optional[str]] = mapped_column(JSON, nullable=True, comment="来自和风天气")
    day_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # 关联
    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="days_list")
    activities: Mapped[list["DayActivity"]] = relationship(
        "DayActivity", back_populates="day", cascade="all, delete-orphan",
        order_by="DayActivity.sort_order",
    )


class DayActivity(Base, TimestampMixin):
    """日程活动表 — 对应 init_db.sql §5 day_activities"""
    __tablename__ = "day_activities"

    day_id: Mapped[str] = mapped_column(String(36), ForeignKey("itinerary_days.id", ondelete="CASCADE"), nullable=False)
    activity_type: Mapped[str] = mapped_column(
        Enum("attraction", "hotel", "restaurant", "transport", "other", name="activity_type"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    address: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    latitude: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 7), nullable=True)
    longitude: Mapped[Optional[float]] = mapped_column(DECIMAL(10, 7), nullable=True)
    duration_minutes: Mapped[int] = mapped_column(Integer, default=60)
    estimated_cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=0)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    transportation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, comment="walk/drive/bus/metro/taxi")
    travel_time_from_prev: Mapped[int] = mapped_column(Integer, default=0, comment="从上个活动过来的交通时间（分钟）")
    ai_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True, comment="AI 推荐理由")
    extra_data: Mapped[Optional[str]] = mapped_column("metadata", JSON, nullable=True, comment="扩展字段")

    # 关联
    day: Mapped["ItineraryDay"] = relationship("ItineraryDay", back_populates="activities")


class ItineraryVersion(Base, TimestampMixin):
    """行程版本表 — 对应 init_db.sql §6 itinerary_versions"""
    __tablename__ = "itinerary_versions"

    itinerary_id: Mapped[str] = mapped_column(String(36), ForeignKey("itineraries.id", ondelete="CASCADE"), nullable=False)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    change_description: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    snapshot: Mapped[str] = mapped_column(JSON, nullable=False, comment="完整行程快照")
    trigger_event: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, comment="user_edit / ai_replan / flight_delay")

    # 关联
    itinerary: Mapped["Itinerary"] = relationship("Itinerary", back_populates="versions")
