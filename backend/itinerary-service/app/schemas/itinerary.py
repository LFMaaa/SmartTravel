from datetime import date as date_type, time
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


# ---------- 活动项 ----------
class ActivityItem(BaseModel):
    id: str = ""
    type: str  # attraction / restaurant / hotel / transport
    name: str
    description: str = ""
    address: str = ""
    lat: float = 0.0
    lng: float = 0.0
    start_time: str = ""  # "09:00"
    end_time: str = ""    # "10:30"
    price: float = 0.0
    tags: list[str] = []
    notes: str = ""


# ---------- 单日行程 ----------
class DayItinerary(BaseModel):
    day_index: int  # 第几天 (1-based)
    date: Optional[date_type] = None
    activities: list[ActivityItem] = []
    hotel: Optional[ActivityItem] = None


# ---------- 行程 ----------
class ItineraryCreateRequest(BaseModel):
    title: str
    destination: str
    start_date: Optional[date_type] = None
    end_date: Optional[date_type] = None
    budget: float = 0
    preferences: list[str] = []  # ["美食", "历史文化"]
    constraints: list[str] = []  # ["不爬山", "腿脚不好"]
    days: list[DayItinerary] = []


class ItineraryResponse(ItineraryCreateRequest):
    id: str
    user_id: str
    status: str = "draft"  # draft / confirmed / in_progress / completed
    total_price: float = 0.0
    version: int = 1
    created_at: str = ""
    updated_at: str = ""