import json
import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.itinerary import Itinerary, ItineraryDay, DayActivity, ItineraryVersion


class ItineraryCRUDService:
    """行程 CRUD 服务 — MySQL 持久化"""

    # ==================== 创建 ====================

    @staticmethod
    async def create_itinerary(
        db: AsyncSession,
        user_id: str,
        title: str,
        destination: str,
        days_data: list[dict],
        start_date: date | None = None,
        end_date: date | None = None,
        total_budget: float | None = None,
        status: str = "draft",
        source: str = "ai_generated",
        dify_workflow_run_id: str | None = None,
        raw_input: str | None = None,
    ) -> dict:
        """创建行程（含天和活动）"""
        itinerary_id = str(uuid.uuid4())

        itinerary = Itinerary(
            id=itinerary_id,
            user_id=user_id,
            title=title,
            destination=destination,
            start_date=start_date,
            end_date=end_date,
            days=len(days_data),
            total_budget=Decimal(str(total_budget)) if total_budget else None,
            status=status,
            source=source,
            dify_workflow_run_id=dify_workflow_run_id,
            raw_input=raw_input,
        )
        db.add(itinerary)

        # 创建天和活动
        for day_data in days_data:
            day = ItineraryDay(
                id=str(uuid.uuid4()),
                itinerary_id=itinerary_id,
                day_number=day_data.get("day_index", day_data.get("day_number", 1)),
                date=day_data.get("date"),
                weather=day_data.get("weather"),
                day_notes=day_data.get("day_notes"),
            )
            db.add(day)

            for i, act_data in enumerate(day_data.get("activities", [])):
                activity = DayActivity(
                    id=act_data.get("id", str(uuid.uuid4())),
                    day_id=day.id,
                    activity_type=act_data.get("type", act_data.get("activity_type", "attraction")),
                    name=act_data.get("name", ""),
                    address=act_data.get("address"),
                    latitude=act_data.get("lat") or act_data.get("latitude"),
                    longitude=act_data.get("lng") or act_data.get("longitude"),
                    duration_minutes=act_data.get("duration_minutes", 60),
                    estimated_cost=Decimal(str(act_data.get("price", act_data.get("estimated_cost", 0)))),
                    sort_order=i + 1,
                    transportation=act_data.get("transportation"),
                    travel_time_from_prev=act_data.get("travel_time_from_prev", 0),
                    ai_reason=act_data.get("ai_reason"),
                    metadata=act_data.get("metadata") or act_data.get("tags"),
                )
                db.add(activity)

            # 处理酒店信息（如果 day_data 中有 hotel 字段）
            if day_data.get("hotel"):
                hotel = day_data["hotel"]
                hotel_activity = DayActivity(
                    id=hotel.get("id", str(uuid.uuid4())),
                    day_id=day.id,
                    activity_type="hotel",
                    name=hotel.get("name", ""),
                    address=hotel.get("address"),
                    latitude=hotel.get("lat") or hotel.get("latitude"),
                    longitude=hotel.get("lng") or hotel.get("longitude"),
                    duration_minutes=0,
                    estimated_cost=Decimal(str(hotel.get("price", 0))),
                    sort_order=0,
                    metadata=hotel.get("tags"),
                )
                db.add(hotel_activity)

        # 创建初始版本快照
        await ItineraryCRUDService._create_version_snapshot(
            db, itinerary_id, version_number=1,
            change_description="AI 初始生成",
            trigger_event="ai_generated",
        )

        await db.flush()
        return ItineraryCRUDService._itinerary_to_dict(itinerary)

    # ==================== 读取 ====================

    @staticmethod
    async def get_itinerary(db: AsyncSession, itinerary_id: str) -> dict:
        """获取行程详情（含天和活动）"""
        result = await db.execute(
            select(Itinerary).where(Itinerary.id == itinerary_id)
        )
        itinerary = result.scalar_one_or_none()
        if not itinerary:
            raise HTTPException(status_code=404, detail="行程不存在")
        return ItineraryCRUDService._itinerary_to_dict(itinerary)

    @staticmethod
    async def list_itineraries(
        db: AsyncSession, user_id: str, page: int = 1, page_size: int = 10,
        status: str | None = None,
    ) -> dict:
        """获取用户行程列表（分页）"""
        query = select(Itinerary).where(Itinerary.user_id == user_id)
        count_query = select(func.count(Itinerary.id)).where(Itinerary.user_id == user_id)

        if status:
            query = query.where(Itinerary.status == status)
            count_query = count_query.where(Itinerary.status == status)

        # 计数
        count_result = await db.execute(count_query)
        total = count_result.scalar() or 0

        # 分页
        offset = (page - 1) * page_size
        result = await db.execute(
            query.order_by(Itinerary.created_at.desc()).offset(offset).limit(page_size)
        )
        itineraries = result.scalars().all()

        return {
            "items": [ItineraryCRUDService._itinerary_to_dict(it) for it in itineraries],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    # ==================== 更新 ====================

    @staticmethod
    async def update_itinerary(db: AsyncSession, itinerary_id: str, update_data: dict) -> dict:
        """更新行程（编辑后保存，创建新版本）"""
        result = await db.execute(select(Itinerary).where(Itinerary.id == itinerary_id))
        itinerary = result.scalar_one_or_none()
        if not itinerary:
            raise HTTPException(status_code=404, detail="行程不存在")

        # 更新基本信息
        for field in ["title", "start_date", "end_date", "total_budget", "status"]:
            if field in update_data and update_data[field] is not None:
                setattr(itinerary, field, update_data[field])

        # 如果提供了新的天数据，替换旧的天和活动
        if "days" in update_data:
            # 删除旧的天和活动
            old_days = await db.execute(
                select(ItineraryDay).where(ItineraryDay.itinerary_id == itinerary_id)
            )
            for old_day in old_days.scalars().all():
                await db.delete(old_day)
            await db.flush()

            # 创建新的天和活动
            for day_data in update_data["days"]:
                day = ItineraryDay(
                    id=str(uuid.uuid4()),
                    itinerary_id=itinerary_id,
                    day_number=day_data.get("day_index", day_data.get("day_number", 1)),
                    date=day_data.get("date"),
                    weather=day_data.get("weather"),
                    day_notes=day_data.get("day_notes"),
                )
                db.add(day)

                for i, act_data in enumerate(day_data.get("activities", [])):
                    activity = DayActivity(
                        id=act_data.get("id", str(uuid.uuid4())),
                        day_id=day.id,
                        activity_type=act_data.get("type", act_data.get("activity_type", "attraction")),
                        name=act_data.get("name", ""),
                        address=act_data.get("address"),
                        latitude=act_data.get("lat") or act_data.get("latitude"),
                        longitude=act_data.get("lng") or act_data.get("longitude"),
                        duration_minutes=act_data.get("duration_minutes", 60),
                        estimated_cost=Decimal(str(act_data.get("price", act_data.get("estimated_cost", 0)))),
                        sort_order=i + 1,
                        transportation=act_data.get("transportation"),
                        travel_time_from_prev=act_data.get("travel_time_from_prev", 0),
                        ai_reason=act_data.get("ai_reason"),
                        metadata=act_data.get("metadata") or act_data.get("tags"),
                    )
                    db.add(activity)

                if day_data.get("hotel"):
                    hotel = day_data["hotel"]
                    hotel_activity = DayActivity(
                        id=hotel.get("id", str(uuid.uuid4())),
                        day_id=day.id,
                        activity_type="hotel",
                        name=hotel.get("name", ""),
                        address=hotel.get("address"),
                        latitude=hotel.get("lat") or hotel.get("latitude"),
                        longitude=hotel.get("lng") or hotel.get("longitude"),
                        duration_minutes=0,
                        estimated_cost=Decimal(str(hotel.get("price", 0))),
                        sort_order=0,
                        metadata=hotel.get("tags"),
                    )
                    db.add(hotel_activity)

            itinerary.days = len(update_data["days"])

        # 创建新版本快照
        latest_version = await db.execute(
            select(func.max(ItineraryVersion.version_number)).where(
                ItineraryVersion.itinerary_id == itinerary_id
            )
        )
        current_version = latest_version.scalar() or 0
        await ItineraryCRUDService._create_version_snapshot(
            db, itinerary_id,
            version_number=current_version + 1,
            change_description=update_data.get("change_description", "用户编辑"),
            trigger_event="user_edit",
        )

        await db.flush()
        return ItineraryCRUDService._itinerary_to_dict(itinerary)

    # ==================== 删除 ====================

    @staticmethod
    async def delete_itinerary(db: AsyncSession, itinerary_id: str) -> None:
        """删除行程（级联删除天、活动、版本）"""
        result = await db.execute(select(Itinerary).where(Itinerary.id == itinerary_id))
        itinerary = result.scalar_one_or_none()
        if not itinerary:
            raise HTTPException(status_code=404, detail="行程不存在")
        await db.delete(itinerary)
        await db.flush()

    # ==================== 版本管理 ====================

    @staticmethod
    async def get_versions(db: AsyncSession, itinerary_id: str) -> list[dict]:
        """获取行程版本历史"""
        result = await db.execute(
            select(ItineraryVersion)
            .where(ItineraryVersion.itinerary_id == itinerary_id)
            .order_by(ItineraryVersion.version_number.desc())
        )
        versions = result.scalars().all()
        return [
            {
                "id": v.id,
                "version_number": v.version_number,
                "change_description": v.change_description,
                "trigger_event": v.trigger_event,
                "created_at": v.created_at.isoformat() if v.created_at else None,
            }
            for v in versions
        ]

    @staticmethod
    async def restore_version(db: AsyncSession, itinerary_id: str, version_number: int) -> dict:
        """恢复到指定版本"""
        result = await db.execute(
            select(ItineraryVersion).where(
                ItineraryVersion.itinerary_id == itinerary_id,
                ItineraryVersion.version_number == version_number,
            )
        )
        version = result.scalar_one_or_none()
        if not version:
            raise HTTPException(status_code=404, detail="版本不存在")

        snapshot = version.snapshot if isinstance(version.snapshot, dict) else json.loads(version.snapshot)
        if "days" in snapshot:
            return await ItineraryCRUDService.update_itinerary(
                db, itinerary_id,
                {
                    "days": snapshot["days"],
                    "change_description": f"恢复到版本 {version_number}",
                }
            )
        raise HTTPException(status_code=400, detail="版本快照数据异常")

    # ==================== 内部工具 ====================

    @staticmethod
    async def _create_version_snapshot(
        db, itinerary_id: str,
        version_number: int,
        change_description: str = "",
        trigger_event: str = "",
    ) -> ItineraryVersion:
        """创建行程版本快照"""
        # 获取当前完整行程数据
        result = await db.execute(select(Itinerary).where(Itinerary.id == itinerary_id))
        itinerary = result.scalar_one_or_none()
        if not itinerary:
            return None

        snapshot = ItineraryCRUDService._itinerary_to_dict(itinerary)

        version = ItineraryVersion(
            id=str(uuid.uuid4()),
            itinerary_id=itinerary_id,
            version_number=version_number,
            change_description=change_description,
            snapshot=snapshot,
            trigger_event=trigger_event,
        )
        db.add(version)
        return version

    @staticmethod
    def _itinerary_to_dict(itinerary: Itinerary) -> dict:
        return {
            "id": itinerary.id,
            "user_id": itinerary.user_id,
            "title": itinerary.title,
            "destination": itinerary.destination,
            "start_date": itinerary.start_date.isoformat() if itinerary.start_date else None,
            "end_date": itinerary.end_date.isoformat() if itinerary.end_date else None,
            "days_count": itinerary.days,
            "total_budget": float(itinerary.total_budget) if itinerary.total_budget else None,
            "status": itinerary.status,
            "source": itinerary.source,
            "dify_workflow_run_id": itinerary.dify_workflow_run_id,
            "raw_input": itinerary.raw_input,
            "created_at": itinerary.created_at.isoformat() if itinerary.created_at else None,
            "updated_at": itinerary.updated_at.isoformat() if itinerary.updated_at else None,
            "version": 1,
            "days": [
                {
                    "id": day.id,
                    "day_index": day.day_number,
                    "day_number": day.day_number,
                    "date": day.date.isoformat() if day.date else None,
                    "weather": day.weather,
                    "day_notes": day.day_notes,
                    "activities": [
                        {
                            "id": act.id,
                            "type": act.activity_type,
                            "name": act.name,
                            "description": act.ai_reason,
                            "address": act.address,
                            "lat": float(act.latitude) if act.latitude else None,
                            "lng": float(act.longitude) if act.longitude else None,
                            "latitude": float(act.latitude) if act.latitude else None,
                            "longitude": float(act.longitude) if act.longitude else None,
                            "start_time": None,
                            "end_time": None,
                            "duration_minutes": act.duration_minutes,
                            "price": float(act.estimated_cost),
                            "estimated_cost": float(act.estimated_cost),
                            "sort_order": act.sort_order,
                            "transportation": act.transportation,
                            "travel_time_from_prev": act.travel_time_from_prev,
                            "ai_reason": act.ai_reason,
                            "tags": act.metadata if isinstance(act.metadata, list) else [],
                            "metadata": act.metadata,
                        }
                        for act in (day.activities or []) if act.activity_type != "hotel"
                    ],
                    "hotel": next(
                        ({
                            "id": act.id,
                            "name": act.name,
                            "address": act.address,
                            "lat": float(act.latitude) if act.latitude else None,
                            "lng": float(act.longitude) if act.longitude else None,
                            "price": float(act.estimated_cost),
                            "tags": act.metadata if isinstance(act.metadata, list) else [],
                        })
                        for act in (day.activities or []) if act.activity_type == "hotel"
                    ),
                }
                for day in (itinerary.days_list or [])
            ],
        }
