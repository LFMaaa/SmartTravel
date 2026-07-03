"""
AI 行程生成服务 — LangChain + DeepSeek V3

工作流:
  用户自然语言 → 意图解析(LLM) → 行程生成(Agent + POI Tool) → 完整行程 JSON

降级策略:
  LLM 不可用 → 返回模拟行程数据
"""
import json
import uuid
import logging
import traceback
from datetime import date, timedelta
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from .llm_service import check_llm_health, is_llm_available
from .intent_parser import parse_intent
from .itinerary_generator import generate_itinerary
from .itinerary_crud_service import ItineraryCRUDService
from .replan_service import ReplanService

logger = logging.getLogger(__name__)


class AIService:
    """AI 行程生成服务 — LangChain + DeepSeek V3"""

    # 重排关键词
    REPLAN_KEYWORDS = [
        "天气", "下雨", "暴雨", "台风", "太热", "太冷", "高温", "降温",
        "下雪", "暴晒", "恶劣天气", "航班", "延误", "飞机", "停飞", "取消",
        "身体", "不舒服", "生病", "头疼", "发烧", "感冒", "健康",
        "修改", "调整", "关闭", "不行", "去不了", "变更", "变化",
        "重新安排", "重排", "换个", "替代", "替代方案", "怎么办",
        "没法去", "计划取消", "不想去了", "去不成了",
    ]

    @staticmethod
    async def generate(
        db: AsyncSession | None, user_id: str, query: str, itinerary_id: str = "",
    ) -> dict:
        """生成行程"""
        # 重排检测
        if itinerary_id and AIService._is_replan_intent(query):
            logger.info(f"[AI] 重排意图: {query[:80]}")
            try:
                return await AIService._route_replan(db, user_id, query, itinerary_id)
            except Exception as e:
                logger.warning(f"[AI] 重排失败: {e}")
                event_type, event_detail = AIService._extract_replan_params(query)
                return {
                    "itinerary_id": itinerary_id, "type": "replan",
                    "event_type": event_type, "event_detail": event_detail,
                    "event_description": query,
                    "alternatives": ReplanService._fallback_alternatives(event_type),
                    "workflow_run_id": None,
                }

        # LLM 健康检查
        llm_ok = await check_llm_health()
        if not llm_ok:
            logger.warning("[AI] LLM 不可用，使用 mock")
            return await AIService._generate_mock(db, user_id, query)

        try:
            return await AIService._generate_via_llm(db, user_id, query)
        except Exception as e:
            logger.warning(f"[AI] LLM 生成失败: {e}")
            traceback.print_exc()
            return await AIService._generate_mock(db, user_id, query)

    @staticmethod
    async def _generate_via_llm(db: AsyncSession | None, user_id: str, query: str) -> dict:
        """LangChain 两阶段生成"""
        # Step 1: 意图解析
        logger.info(f"[AI] Step 1 — 意图解析: {query[:80]}")
        intent = await parse_intent(query)

        # Step 2: 行程生成（Agent + POI Tool Calling）
        logger.info(f"[AI] Step 2 — 行程生成: {intent}")
        itinerary = await generate_itinerary(intent)

        destination = itinerary.get("destination", intent.get("destination", ""))
        total_budget = itinerary.get("total_budget", intent.get("budget", 0))
        days_data = itinerary.get("days", [])

        itinerary_data = {
            "title": f"AI定制行程 - {destination}",
            "destination": destination,
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=len(days_data) - 1)).isoformat(),
            "total_budget": total_budget,
            "days": days_data,
            "status": "draft",
            "source": "ai_generated",
            "dify_workflow_run_id": None,
            "raw_input": {"query": query, "intent": intent},
        }

        if db is None:
            return itinerary_data

        return await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id, title=itinerary_data["title"],
            destination=itinerary_data["destination"],
            days_data=itinerary_data["days"],
            start_date=itinerary_data["start_date"],
            end_date=itinerary_data["end_date"],
            total_budget=itinerary_data["total_budget"],
            status="draft", source="ai_generated",
            raw_input=itinerary_data["raw_input"],
        )

    # ==================== SSE 流式 ====================

    @staticmethod
    async def generate_stream(
        db: AsyncSession, user_id: str, query: str, itinerary_id: str = "",
    ) -> AsyncGenerator[str, None]:
        if itinerary_id and AIService._is_replan_intent(query):
            try:
                result = await AIService._route_replan(db, user_id, query, itinerary_id)
                yield AIService._sse("thinking", "检测到行程变更需求，正在生成备选方案...")
                yield AIService._sse("done", result)
                return
            except Exception:
                pass

        llm_ok = await check_llm_health()
        if not llm_ok:
            async for event in AIService._generate_stream_mock(db, user_id, query):
                yield event
            return

        try:
            async for event in AIService._generate_stream_via_llm(db, user_id, query):
                yield event
        except Exception:
            async for event in AIService._generate_stream_mock(db, user_id, query):
                yield event

    @staticmethod
    async def _generate_stream_via_llm(
        db: AsyncSession, user_id: str, query: str,
    ) -> AsyncGenerator[str, None]:
        yield AIService._sse("thinking", "正在解析您的出行意图...")
        intent = await parse_intent(query)
        yield AIService._sse("thinking",
            f"解析完成：目的地 {intent.get('destination', '未知')}，{intent.get('days', 3)} 天")

        yield AIService._sse("thinking", "AI 正在规划每日行程...")
        itinerary = await generate_itinerary(intent)

        days_data = itinerary.get("days", [])
        destination = itinerary.get("destination", "")
        total_budget = itinerary.get("total_budget", 0)

        yield AIService._sse("thinking", f"正在保存行程数据（{len(days_data)}天，¥{total_budget}）...")

        saved = await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id,
            title=f"AI定制行程 - {destination}",
            destination=destination,
            days_data=days_data,
            start_date=date.today().isoformat(),
            end_date=(date.today() + timedelta(days=len(days_data) - 1)).isoformat(),
            total_budget=total_budget,
            status="draft", source="ai_generated",
            raw_input={"query": query, "intent": intent},
        )
        yield AIService._sse("done", {"itinerary_id": saved["id"], "data": saved})

    # ==================== Mock 降级 ====================

    @staticmethod
    async def _generate_mock(db: AsyncSession | None, user_id: str, query: str) -> dict:
        mock = AIService._build_mock(query)
        if db is None:
            return mock
        return await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id, title=mock["title"],
            destination=mock["destination"], days_data=mock["days"],
            start_date=mock["start_date"], end_date=mock["end_date"],
            total_budget=mock["total_budget"],
            status="draft", source="ai_generated", raw_input=query,
        )

    @staticmethod
    async def _generate_stream_mock(
        db: AsyncSession, user_id: str, query: str,
    ) -> AsyncGenerator[str, None]:
        steps = ["解析出行意图...", "匹配目的地数据...", "优化行程路线...", "生成每日安排...", "保存行程数据..."]
        for step in steps:
            yield AIService._sse("thinking", step)
        mock = AIService._build_mock(query)
        saved = await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id, title=mock["title"],
            destination=mock["destination"], days_data=mock["days"],
            start_date=mock["start_date"], end_date=mock["end_date"],
            total_budget=mock["total_budget"],
            status="draft", source="ai_generated", raw_input=query,
        )
        yield AIService._sse("done", {"itinerary_id": saved["id"], "data": saved})

    # ==================== 工具方法 ====================

    @staticmethod
    def _is_replan_intent(query: str) -> bool:
        return any(kw in query for kw in AIService.REPLAN_KEYWORDS)

    @staticmethod
    def _extract_replan_params(query: str) -> tuple[str, dict]:
        q = query
        event_type = "custom"
        event_detail = {"description": q}

        if any(w in q for w in ["天气", "下雨", "暴雨", "下雪", "高温", "太热", "太冷", "降温"]):
            event_type = "weather_alert"
            if "雨" in q:
                event_detail = {"weather_type": "降雨", "affected_time": "明天"}
            elif any(w in q for w in ["热", "高温", "暴晒"]):
                event_detail = {"weather_type": "高温酷暑", "affected_time": "近期"}
            else:
                event_detail = {"weather_type": "异常天气", "affected_time": "近期"}
        elif any(w in q for w in ["航班", "飞机", "延误", "停飞"]):
            event_type = "flight_delay"
            event_detail = {"delay_hours": "未知", "flight_no": "未知"}
        elif any(w in q for w in ["身体", "不舒服", "生病", "头疼", "发烧", "感冒"]):
            event_type = "health_issue"
            event_detail = {"symptom": "身体状态不佳", "recovery_time": "待定"}

        return event_type, event_detail

    @staticmethod
    async def _route_replan(
        db: AsyncSession | None, user_id: str, query: str, itinerary_id: str,
    ) -> dict:
        event_type, event_detail = AIService._extract_replan_params(query)
        if db is not None:
            result = await ReplanService.replan(db, itinerary_id, event_type, event_detail, user_id)
        else:
            result = {
                "itinerary_id": itinerary_id, "event_type": event_type,
                "event_detail": event_detail, "event_description": query,
                "alternatives": ReplanService._fallback_alternatives(event_type),
                "workflow_run_id": None,
            }
        result["type"] = "replan"
        return result

    @staticmethod
    def _sse(event_type: str, data) -> str:
        payload = {"type": event_type}
        if isinstance(data, str):
            payload["content"] = data
        else:
            payload["data"] = data
        return f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"

    @staticmethod
    def _build_mock(query: str) -> dict:
        import re
        known_cities = [
            "北京", "成都", "上海", "杭州", "西安", "大理", "三亚", "云南",
            "新疆", "西藏", "桂林", "厦门", "青岛", "哈尔滨", "长沙", "重庆",
            "武汉", "南京", "苏州", "广州", "深圳", "丽江", "昆明", "贵阳",
        ]
        destination = next((c for c in known_cities if c in query), None)
        if not destination:
            m = re.search(r"去(\w{2,4})(?:玩|旅游|旅行|之旅)?", query)
            destination = m.group(1) if m else "推荐目的地"

        days_count = int(m.group(1)) if (m := re.search(r"(\d+)\s*天", query)) else 3
        budget = int(m.group(1)) if (m := re.search(r"预算.*?(\d+)", query)) else 3000

        start_date = date.today()
        days = []
        for d in range(days_count):
            activities = [
                {"id": str(uuid.uuid4()), "type": "attraction",
                 "name": f"{destination}推荐景点{d+1}", "address": f"{destination}市中心",
                 "start_time": "09:00", "duration": "120分钟", "price": budget // (days_count * 4),
                 "tags": ["推荐"]},
                {"id": str(uuid.uuid4()), "type": "restaurant",
                 "name": f"{destination}特色餐厅", "address": f"{destination}市中心",
                 "start_time": "12:00", "duration": "60分钟", "price": budget // (days_count * 5),
                 "tags": ["美食"]},
            ]
            hotel = {"id": str(uuid.uuid4()), "name": f"{destination}舒适酒店",
                     "address": f"{destination}市中心", "price": budget // (days_count * 3)}
            days.append({
                "day_index": d + 1,
                "date": (start_date + timedelta(days=d)).isoformat(),
                "activities": activities,
                "hotel": hotel,
            })

        return {
            "title": f"AI定制行程 - {query[:30]}",
            "destination": destination,
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=days_count - 1)).isoformat(),
            "total_budget": budget,
            "days": days,
        }
