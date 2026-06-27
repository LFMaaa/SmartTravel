import json
import uuid
import logging
from datetime import date, timedelta

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from common.schemas import APIResponse

from ..database import get_db, is_db_available
from ..services.ai_service import AIService
from ..services.replan_service import ReplanService
from ..services.itinerary_crud_service import ItineraryCRUDService
from ..schemas.itinerary import ItineraryResponse, ItineraryCreateRequest

router = APIRouter()
logger = logging.getLogger(__name__)

# In-memory storage fallback when MySQL is unavailable
_memory_store: dict[str, dict] = {}


# ---------- Request models ----------
class GenerateRequest(BaseModel):
    query: str
    user_id: str = "anonymous"
    itinerary_id: str = ""  # 非空时可能触发动态重排


class ReplanRequest(BaseModel):
    itinerary_id: str
    event_type: str
    event_detail: dict = {}


class ApplyReplanRequest(BaseModel):
    plan_id: str
    itinerary_id: str


# ---------- Routes ----------

@router.post("/generate", response_model=APIResponse)
async def generate_itinerary(req: GenerateRequest):
    """AI 智能行程生成 — 优先 Dify，不可用时降级 mock"""
    if is_db_available():
        from ..database import async_session_factory
        async with async_session_factory() as db:
            try:
                itinerary = await AIService.generate(db, req.user_id, req.query, req.itinerary_id)
                await db.commit()
                return APIResponse(data=itinerary)
            except Exception:
                await db.rollback()
                raise
    else:
        # Memory mode: still try Dify first, save to memory
        itinerary = await AIService.generate(None, req.user_id, req.query, req.itinerary_id)
        itinerary_id = itinerary.get("id") or str(uuid.uuid4())
        if "id" not in itinerary:
            itinerary["id"] = itinerary_id
        if "user_id" not in itinerary:
            itinerary["user_id"] = req.user_id
        if "status" not in itinerary:
            itinerary["status"] = "draft"
        if "version" not in itinerary:
            itinerary["version"] = 1
        if "created_at" not in itinerary:
            itinerary["created_at"] = date.today().isoformat()
        if "updated_at" not in itinerary:
            itinerary["updated_at"] = date.today().isoformat()
        _memory_store[itinerary_id] = itinerary
        return APIResponse(data=itinerary)


@router.post("/generate/stream")
async def generate_itinerary_stream(req: GenerateRequest):
    """AI 行程生成（SSE 流式输出）"""
    if is_db_available():
        from ..database import async_session_factory

        async def stream_with_db():
            async with async_session_factory() as db:
                try:
                    async for event in AIService.generate_stream(db, req.user_id, req.query, req.itinerary_id):
                        yield event
                    await db.commit()
                except Exception:
                    await db.rollback()
                    yield _sse_event("error", "生成失败，请重试")

        return StreamingResponse(stream_with_db(), media_type="text/event-stream")
    else:
        # Memory mode
        async def stream_memory():
            async for event in AIService.generate_stream(None, req.user_id, req.query, req.itinerary_id):
                yield event
            # Save to memory after stream
            mock = AIService._build_mock(req.query)
            itinerary_id = str(uuid.uuid4())
            mock["id"] = itinerary_id
            mock["user_id"] = req.user_id
            mock["status"] = "draft"
            mock["version"] = 1
            mock["created_at"] = date.today().isoformat()
            mock["updated_at"] = date.today().isoformat()
            _memory_store[itinerary_id] = mock
            yield _sse_event("done", {"itinerary_id": itinerary_id, "data": mock})

        return StreamingResponse(stream_memory(), media_type="text/event-stream")


@router.get("/{itinerary_id}", response_model=APIResponse)
async def get_itinerary(itinerary_id: str):
    """获取行程详情"""
    if is_db_available():
        from ..database import async_session_factory
        async with async_session_factory() as db:
            try:
                itinerary = await ItineraryCRUDService.get_itinerary(db, itinerary_id)
                await db.commit()
                return APIResponse(data=itinerary)
            except Exception:
                await db.rollback()
                raise
    else:
        data = _memory_store.get(itinerary_id)
        if not data:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="行程不存在")
        return APIResponse(data=data)


@router.put("/{itinerary_id}", response_model=APIResponse)
async def update_itinerary(itinerary_id: str, req: ItineraryCreateRequest):
    """更新行程"""
    if is_db_available():
        from ..database import async_session_factory
        async with async_session_factory() as db:
            try:
                update_data = req.model_dump(exclude_none=True)
                itinerary = await ItineraryCRUDService.update_itinerary(db, itinerary_id, update_data)
                await db.commit()
                return APIResponse(data=itinerary)
            except Exception:
                await db.rollback()
                raise
    else:
        if itinerary_id not in _memory_store:
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="行程不存在")
        _memory_store[itinerary_id].update(req.model_dump(exclude_none=True))
        return APIResponse(data=_memory_store[itinerary_id])


@router.delete("/{itinerary_id}", response_model=APIResponse)
async def delete_itinerary(itinerary_id: str):
    """删除行程"""
    if is_db_available():
        from ..database import async_session_factory
        async with async_session_factory() as db:
            try:
                await ItineraryCRUDService.delete_itinerary(db, itinerary_id)
                await db.commit()
            except Exception:
                await db.rollback()
                raise
    else:
        _memory_store.pop(itinerary_id, None)
    return APIResponse(message="删除成功")


@router.post("/{itinerary_id}/replan", response_model=APIResponse)
async def replan_itinerary(itinerary_id: str, req: ReplanRequest):
    """动态重排行程"""
    if is_db_available():
        from ..database import async_session_factory
        async with async_session_factory() as db:
            try:
                result = await ReplanService.replan(db, itinerary_id, req.event_type, req.event_detail)
                await db.commit()
                return APIResponse(data=result)
            except Exception:
                await db.rollback()
                raise
    else:
        # Memory mode: return mock alternatives
        result = {
            "itinerary_id": itinerary_id,
            "event_type": req.event_type,
            "event_detail": req.event_detail,
            "alternatives": [
                {"plan_id": str(uuid.uuid4()), "title": "方案A：调整行程顺序", "description": "将受影响时段与后续日期对调", "impact": "总行程时间不变"},
                {"plan_id": str(uuid.uuid4()), "title": "方案B：替换为备选景点", "description": "推荐同区域相似景点", "impact": "预算增加约¥150"},
                {"plan_id": str(uuid.uuid4()), "title": "方案C：顺延+优化", "description": "整体顺延行程", "impact": "预算增加约¥500"},
            ],
        }
        return APIResponse(data=result)


@router.get("/", response_model=APIResponse)
async def list_itineraries(
    user_id: str = Query(..., description="用户ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    status: str | None = Query(None, description="行程状态筛选"),
):
    """获取用户的行程列表"""
    if is_db_available():
        from ..database import async_session_factory
        async with async_session_factory() as db:
            try:
                result = await ItineraryCRUDService.list_itineraries(db, user_id, page, page_size, status)
                await db.commit()
                return APIResponse(data=result)
            except Exception:
                await db.rollback()
                raise
    else:
        items = [v for v in _memory_store.values() if v.get("user_id") == user_id]
        return APIResponse(data={
            "items": items[(page - 1) * page_size: page * page_size],
            "total": len(items),
            "page": page,
            "page_size": page_size,
        })


# ---------- Helpers ----------

async def _generate_memory(user_id: str, query: str) -> dict:
    """内存模式：生成模拟行程"""
    mock = AIService._build_mock(query)
    itinerary_id = str(uuid.uuid4())
    mock["id"] = itinerary_id
    mock["user_id"] = user_id
    mock["status"] = "draft"
    mock["version"] = 1
    mock["created_at"] = date.today().isoformat()
    mock["updated_at"] = date.today().isoformat()
    _memory_store[itinerary_id] = mock
    return mock


def _sse_event(event_type: str, data) -> str:
    payload = {"type": event_type}
    if isinstance(data, str):
        payload["content"] = data
    else:
        payload["data"] = data
    return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
