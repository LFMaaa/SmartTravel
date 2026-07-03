"""
动态重排服务 — LangChain Agent

流程:
  当前行程 + 事件描述 → LLM → 多套备选方案

输出:
  { alternatives: [{ plan_id, title, description, impact, changes }] }
"""
import json
import logging
import uuid
from typing import Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from sqlalchemy.ext.asyncio import AsyncSession

from .llm_service import get_llm, is_llm_available
from .itinerary_crud_service import ItineraryCRUDService

logger = logging.getLogger(__name__)

REPLAN_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的旅行应急规划助手。根据当前行程和突发事件的描述，生成 3 套可行的备选方案。

输出严格的 JSON 格式（不要 markdown 代码块）:
{{
  "alternatives": [
    {{
      "plan_id": "plan_1",
      "title": "方案A：简短标题",
      "description": "方案详细描述（50-100字）",
      "impact": "对行程的影响评估（如'预算不变，行程时间顺延半天'）",
      "changes": ["具体变更1", "具体变更2"]
    }},
    ...
  ]
}}

规则:
- 方案A：保守方案（最小影响，如调整活动顺序、替换同区域景点）
- 方案B：平衡方案（适度调整，如替换为备选城市活动）
- 方案C：激进方案（完全重构，如取消当天改为室内/休闲活动）
- 每个方案给出具体的预算影响和行程变更
- 直接输出 JSON，不要有其他文字"""),
    ("human", """当前行程:
目的地: {destination}
行程天数: {days}天
当前日期: {current_date}

行程详情:
{itinerary_summary}

突发事件:
类型: {event_type}
详情: {event_description}

请生成 3 套备选方案。"""),
])

REPLAN_OUTPUT_PARSER = StrOutputParser()


class ReplanService:
    """动态重排服务 — LangChain 实现"""

    @staticmethod
    async def replan(
        db: AsyncSession,
        itinerary_id: str,
        event_type: str,
        event_detail: dict,
        user_id: str = "smarttravel-user",
    ) -> dict:
        """生成备选方案"""
        # Step 1: 获取当前行程
        itinerary = await ItineraryCRUDService.get_itinerary(db, itinerary_id)
        if not itinerary:
            raise RuntimeError(f"行程不存在: {itinerary_id}")

        # 构建事件描述
        event_description = ReplanService._build_event_description(event_type, event_detail)
        itinerary_summary = ReplanService._summarize_itinerary(itinerary)

        # Step 2: 调用 LLM 生成方案
        if not is_llm_available():
            logger.warning("[Replan] LLM 不可用，使用降级方案")
            return ReplanService._build_fallback(itinerary_id, event_type, event_detail, event_description)

        try:
            llm = get_llm(temperature=0.5, max_tokens=4096)
            chain = REPLAN_PROMPT | llm | REPLAN_OUTPUT_PARSER

            result = await chain.ainvoke({
                "destination": itinerary.get("destination", ""),
                "days": itinerary.get("days", 1),
                "current_date": itinerary.get("start_date", "2026-07-01"),
                "itinerary_summary": itinerary_summary,
                "event_type": event_type,
                "event_description": event_description,
            })

            result = result.strip()
            if result.startswith("```"):
                parts = result.split("```")
                result = parts[1]
                if result.startswith("json"):
                    result = result[4:]
                result = result.strip()

            data = json.loads(result)
            alternatives = data.get("alternatives", [])

        except Exception as e:
            logger.warning(f"[Replan] LLM 调用失败: {e}，使用降级方案")
            alternatives = ReplanService._fallback_alternatives(event_type)

        # Step 3: 记录版本快照
        try:
            await ItineraryCRUDService._create_version_snapshot(
                db, itinerary_id,
                version_number=1,
                change_description=f"触发事件: {event_type} — {event_description}",
                trigger_event=event_type,
            )
        except Exception:
            pass

        return {
            "itinerary_id": itinerary_id,
            "event_type": event_type,
            "event_detail": event_detail,
            "event_description": event_description,
            "alternatives": alternatives,
            "workflow_run_id": None,
        }

    @staticmethod
    def _build_fallback(itinerary_id, event_type, event_detail, event_description) -> dict:
        return {
            "itinerary_id": itinerary_id,
            "event_type": event_type,
            "event_detail": event_detail,
            "event_description": event_description,
            "alternatives": ReplanService._fallback_alternatives(event_type),
            "workflow_run_id": None,
        }

    @staticmethod
    def _summarize_itinerary(itinerary: dict) -> str:
        """将行程 JSON 压缩为文本摘要"""
        parts = []
        for day in itinerary.get("days", []):
            acts = ", ".join(
                f"{a.get('name', '')}({a.get('start_time', '')})"
                for a in day.get("activities", [])
            )
            hotel = day.get("hotel", {})
            hotel_str = f" → 住 {hotel.get('name', '未定')}(¥{hotel.get('price', 0)})" if hotel else ""
            parts.append(f"第{day.get('day_index', '?')}天: {acts}{hotel_str}")
        return "\n".join(parts)

    @staticmethod
    def _build_event_description(event_type: str, event_detail: dict) -> str:
        templates = {
            "flight_delay": "航班延误{delay_hours}小时（航班号：{flight_no}）",
            "weather_alert": "天气预警：{weather_type}，影响时段：{affected_time}",
            "attraction_closed": "景点关闭：{attraction_name}，原因：{reason}",
            "health_issue": "身体不适：{symptom}，预计恢复时间：{recovery_time}",
            "custom": "{description}",
        }
        template = templates.get(event_type, "行程受到影响：{event_type}")
        try:
            return template.format(**event_detail, event_type=event_type)
        except KeyError:
            return f"{event_type}: {json.dumps(event_detail, ensure_ascii=False)}"

    @staticmethod
    def _fallback_alternatives(event_type: str) -> list[dict]:
        return [
            {
                "plan_id": str(uuid.uuid4()),
                "title": "方案A：调整行程顺序",
                "description": f"将受「{event_type}」影响的时段与后续日期对调，保持原有行程内容不变",
                "impact": "总行程时间不变，无需额外费用",
                "changes": ["对调受影响时段与后续日期"],
            },
            {
                "plan_id": str(uuid.uuid4()),
                "title": "方案B：替换为备选景点",
                "description": "推荐同区域内的相似景点或室内活动作为替代方案",
                "impact": "预算增加约 ¥150，行程时间不变",
                "changes": ["替换受影响景点", "新增备选活动"],
            },
            {
                "plan_id": str(uuid.uuid4()),
                "title": "方案C：顺延+优化",
                "description": "整体顺延行程一天，重新优化后续路线，增加室内/休闲活动",
                "impact": "酒店需延期1晚，预算增加约 ¥500",
                "changes": ["整体顺延1天", "增加室内活动", "调整酒店"],
            },
        ]
