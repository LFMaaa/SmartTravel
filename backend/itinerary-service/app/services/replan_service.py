"""
动态重排服务

流程：
  行程JSON + 事件(航班延误/天气/关闭等) → 动态重排工作流 → 3套备选方案

Dify 动态重排工作流输入：
  - itinerary: 行程生成工作流的输出（完整行程JSON）
  - event: 触发重排的事件描述（如 "航班延误4小时"）
"""
import json
import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..dify.client import (
    DifyClient,
    get_replan_client,
    get_generator_client,
)
from .itinerary_crud_service import ItineraryCRUDService

logger = logging.getLogger(__name__)


class ReplanService:
    """动态重排服务 — 调用 Dify 动态重排工作流"""

    @staticmethod
    async def replan(
        db: AsyncSession,
        itinerary_id: str,
        event_type: str,
        event_detail: dict,
        user_id: str = "smarttravel-user",
    ) -> dict:
        """根据事件类型调用 Dify 动态重排工作流生成备选方案

        Args:
            db: 数据库会话
            itinerary_id: 当前行程 ID
            event_type: 事件类型 (flight_delay / weather_alert / attraction_closed / custom)
            event_detail: 事件详情 (如 {"delay_hours": 4, "flight_no": "CA1234"})

        Returns:
            {
                "itinerary_id": ...,
                "event_type": ...,
                "alternatives": [ {plan_id, title, description, impact, changes}, ... ]
            }
        """
        # ---- Step 1: 获取当前行程数据 ----
        itinerary = await ItineraryCRUDService.get_itinerary(db, itinerary_id)
        if not itinerary:
            raise RuntimeError(f"行程不存在: {itinerary_id}")

        # ---- Step 2: 构建事件描述 ----
        event_description = ReplanService._build_event_description(event_type, event_detail)
        logger.info(f"[Replan] 事件: {event_type} — {event_description}")

        # ---- Step 3: 调用动态重排工作流 ----
        # 输入1: 当前行程（行程生成工作流的输出）
        # 输入2: 事件描述
        replan_client = get_replan_client()

        replan_inputs = {
            "itinerary": json.dumps(itinerary, ensure_ascii=False),
            "event": event_description,
            "event_type": event_type,
        }

        logger.info(f"[Replan] 调用动态重排工作流...")
        replan_result = await replan_client.run_workflow(
            inputs=replan_inputs,
            user=user_id,
            response_mode="blocking",
        )

        # ---- Step 4: 解析备选方案 ----
        outputs = DifyClient.extract_outputs(replan_result)
        alternatives = outputs.get("alternatives", outputs.get("plans", []))

        # 如果 alternatives 是 JSON 字符串，尝试解析
        if isinstance(alternatives, str):
            try:
                alternatives = json.loads(alternatives)
            except json.JSONDecodeError:
                logger.warning(f"[Replan] alternatives 解析失败: {alternatives[:200]}")
                alternatives = []

        # 标准化备选方案格式
        normalized = []
        for i, alt in enumerate(alternatives):
            if isinstance(alt, str):
                normalized.append({
                    "plan_id": f"plan_{i+1}",
                    "title": f"方案{chr(65+i)}",
                    "description": alt,
                    "impact": "未知",
                    "changes": [],
                })
            elif isinstance(alt, dict):
                normalized.append({
                    "plan_id": alt.get("plan_id", f"plan_{i+1}"),
                    "title": alt.get("title", f"方案{chr(65+i)}"),
                    "description": alt.get("description", ""),
                    "impact": alt.get("impact", alt.get("cost_impact", "")),
                    "changes": alt.get("changes", []),
                })

        if not normalized:
            logger.warning("[Replan] 工作流未返回有效备选方案，使用兜底方案")
            normalized = ReplanService._fallback_alternatives(event_type)

        logger.info(f"[Replan] 生成 {len(normalized)} 套备选方案")

        # ---- Step 5: 记录版本快照 ----
        await ItineraryCRUDService._create_version_snapshot(
            db, itinerary_id,
            version_number=1,
            change_description=f"触发事件: {event_type} — {event_description}",
            trigger_event=event_type,
        )

        return {
            "itinerary_id": itinerary_id,
            "event_type": event_type,
            "event_detail": event_detail,
            "event_description": event_description,
            "alternatives": normalized,
            "workflow_run_id": replan_result.get("workflow_run_id"),
        }

    # ==================== 工具方法 ====================

    @staticmethod
    def _build_event_description(event_type: str, event_detail: dict) -> str:
        """构建人类可读的事件描述"""
        templates = {
            "flight_delay": "航班延误{delay_hours}小时（航班号：{flight_no}）",
            "weather_alert": "天气预警：{weather_type}，影响时段：{affected_time}",
            "attraction_closed": "景点关闭：{attraction_name}，原因：{reason}",
            "custom": "{description}",
        }
        template = templates.get(event_type, "行程受到影响：{event_type}")
        try:
            return template.format(**event_detail, event_type=event_type)
        except KeyError:
            return f"{event_type}: {json.dumps(event_detail, ensure_ascii=False)}"

    @staticmethod
    def _fallback_alternatives(event_type: str) -> list[dict]:
        """兜底备选方案（Dify 工作流不可用时使用）"""
        import uuid
        return [
            {
                "plan_id": str(uuid.uuid4()),
                "title": "方案A：调整行程顺序",
                "description": f"将受「{event_type}」影响的时段与后续日期对调",
                "impact": "总行程时间不变，无需额外费用",
                "changes": [],
            },
            {
                "plan_id": str(uuid.uuid4()),
                "title": "方案B：替换为备选景点",
                "description": "推荐同区域内的相似景点作为替代",
                "impact": "预算增加约 ¥150",
                "changes": [],
            },
            {
                "plan_id": str(uuid.uuid4()),
                "title": "方案C：顺延+优化",
                "description": "整体顺延行程，重新优化路线",
                "impact": "酒店需延期1晚，预算增加约 ¥500",
                "changes": [],
            },
        ]
