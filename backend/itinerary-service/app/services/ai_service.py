"""
AI 行程生成服务

工作流串联（优先 Dify，不可用时降级到 mock 数据）：
  用户自然语言 → 意图解析工作流 → 行程生成工作流 → 完整行程 JSON

降级策略：
  Dify 不可用 → 返回模拟行程数据（保证前端流程可通）
"""
import json
import uuid
import logging
import traceback
from datetime import date, timedelta
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..dify.client import (
    DifyClient,
    get_intent_client,
    get_generator_client,
    check_dify_health,
)
from .itinerary_crud_service import ItineraryCRUDService
from .replan_service import ReplanService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class AIService:
    """AI 行程生成服务 — 优先 Dify，不可用时降级 mock"""

    @staticmethod
    async def generate(db: AsyncSession | None, user_id: str, query: str, itinerary_id: str = "") -> dict:
        """生成行程，先检测 Dify，不可用则降级 mock

        当 itinerary_id 非空且 query 包含动态重排关键词时，
        自动路由到 ReplanService 调用 Dify 动态重排工作流。
        """
        # ---- 动态重排检测 ----
        if itinerary_id and AIService._is_replan_intent(query):
            logger.info(f"[AI] 检测到重排意图: query='{query[:80]}', itinerary={itinerary_id}")
            try:
                return await AIService._route_replan(db, user_id, query, itinerary_id)
            except Exception as e:
                logger.warning(f"[AI] 重排路由失败: {e}，返回兜底备选方案（不回退到普通生成）")
                # 重要：已确认为重排意图时，即使Dify调用失败也不回退普通生成
                # 否则"明天下大雨取消行程"这类消息会生成垃圾的"默认目的地"行程
                event_type, event_detail = AIService._extract_replan_params(query)
                return {
                    "itinerary_id": itinerary_id,
                    "event_type": event_type,
                    "event_detail": event_detail,
                    "event_description": query,
                    "type": "replan",
                    "alternatives": ReplanService._fallback_alternatives(event_type),
                    "workflow_run_id": None,
                }

        dify_ok = await check_dify_health()
        logger.info(f"[AI] Dify 状态: {'可用' if dify_ok else '不可用，使用 mock'}")

        if not dify_ok:
            return await AIService._generate_mock(db, user_id, query)

        try:
            return await AIService._generate_via_dify(db, user_id, query)
        except Exception as e:
            logger.warning(f"[AI] Dify 调用失败: {e}")
            traceback.print_exc()
            return await AIService._generate_mock(db, user_id, query)

    @staticmethod
    async def _generate_via_dify(db: AsyncSession, user_id: str, query: str) -> dict:
        """通过 Dify 工作流生成"""
        intent_client = get_intent_client()
        generator_client = get_generator_client()

        # Step 1: 意图解析 → 输入 user_query，输出 parsed_intent 字符串
        logger.info(f"[AI] Step 1 — 意图解析: query='{query[:80]}'")
        intent_result = await intent_client.run_workflow(
            inputs={"user_query": query}, user=user_id, response_mode="blocking",
        )
        intent_outputs = DifyClient.extract_outputs(intent_result)
        parsed_intent = intent_outputs.get("parsed_intent", "")
        logger.info(f"[AI] 意图解析输出: {parsed_intent[:200]}")

        # Step 2: 行程生成 → 输入 parsed_intent 字符串，输出 itinerary_json
        logger.info(f"[AI] Step 2 — 行程生成")
        gen_result = await generator_client.run_workflow(
            inputs={"parsed_intent": parsed_intent}, user=user_id, response_mode="blocking",
        )
        gen_outputs = DifyClient.extract_outputs(gen_result)
        logger.info(f"[AI] 行程生成原始输出: destination={gen_outputs.get('destination')}, days={gen_outputs.get('days_count')}, cost={gen_outputs.get('total_cost')}")

        # Step 3: 解析 itinerary_json 自定义格式
        itinerary_json = gen_outputs.get("itinerary_json", "")
        if not itinerary_json:
            logger.warning(f"[AI] 行程生成输出为空, gen_outputs keys={list(gen_outputs.keys())}")
            return await AIService._generate_mock(db, user_id, query)

        days_data = AIService._parse_itinerary_json(itinerary_json)
        if not days_data:
            logger.warning(f"[AI] 无法解析 itinerary_json，回退到 mock")
            return await AIService._generate_mock(db, user_id, query)

        # 从意图解析中提取目的地
        intent_dict = AIService._parse_parsed_intent(parsed_intent)
        destination = gen_outputs.get("destination") or intent_dict.get("destination", "")
        total_budget = int(gen_outputs.get("total_cost", 0))

        logger.info(f"[AI] 行程生成完成: {len(days_data)} 天, destination={destination}, budget={total_budget}")
        
        # 构建行程数据
        itinerary_data = {
            "title": f"AI定制行程 - {destination}",
            "destination": destination,
            "start_date": date.today().isoformat(),
            "end_date": (date.today() + timedelta(days=len(days_data) - 1)).isoformat(),
            "total_budget": total_budget,
            "days": days_data,
            "status": "draft",
            "source": "ai_generated",
            "dify_workflow_run_id": gen_result.get("workflow_run_id"),
            "raw_input": {"query": query, "intent": intent_outputs, "generator": gen_outputs},
        }
        
        if db is None:
            # 内存模式：直接返回，不写数据库
            return itinerary_data
        
        return await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id, title=itinerary_data["title"],
            destination=itinerary_data["destination"],
            days_data=itinerary_data["days"],
            start_date=itinerary_data["start_date"],
            end_date=itinerary_data["end_date"],
            total_budget=itinerary_data["total_budget"],
            status="draft", source="ai_generated",
            dify_workflow_run_id=gen_result.get("workflow_run_id"),
            raw_input=itinerary_data["raw_input"],
        )

    # ==================== SSE 流式 ====================

    @staticmethod
    async def generate_stream(
        db: AsyncSession, user_id: str, query: str, itinerary_id: str = "",
    ) -> AsyncGenerator[str, None]:
        # ---- 动态重排检测 ----
        if itinerary_id and AIService._is_replan_intent(query):
            logger.info(f"[AI Stream] 检测到重排意图: query='{query[:80]}', itinerary={itinerary_id}")
            try:
                result = await AIService._route_replan(db, user_id, query, itinerary_id)
                yield AIService._sse("thinking", f"检测到行程变更需求，正在调用动态重排工作流...")
                yield AIService._sse("done", result)
                return
            except Exception as e:
                logger.warning(f"[AI Stream] 重排路由失败: {e}，返回兜底备选方案")
                event_type, event_detail = AIService._extract_replan_params(query)
                fallback = {
                    "itinerary_id": itinerary_id,
                    "event_type": event_type,
                    "event_detail": event_detail,
                    "event_description": query,
                    "type": "replan",
                    "alternatives": ReplanService._fallback_alternatives(event_type),
                    "workflow_run_id": None,
                }
                yield AIService._sse("thinking", "动态重排工作流暂时不可用，已为您准备兜底备选方案...")
                yield AIService._sse("done", fallback)
                return

        dify_ok = await check_dify_health()
        if not dify_ok:
            async for event in AIService._generate_stream_mock(db, user_id, query):
                yield event
            return

        try:
            async for event in AIService._generate_stream_via_dify(db, user_id, query):
                yield event
        except Exception as e:
            logger.warning(f"[AI] Dify 流式失败: {e}")
            async for event in AIService._generate_stream_mock(db, user_id, query):
                yield event

    @staticmethod
    async def _generate_stream_via_dify(
        db: AsyncSession, user_id: str, query: str,
    ) -> AsyncGenerator[str, None]:
        intent_client = get_intent_client()
        generator_client = get_generator_client()

        yield AIService._sse("thinking", "正在解析您的出行意图...")

        # Step 1: 意图解析（同步）
        intent_result = await intent_client.run_workflow(
            inputs={"user_query": query}, user=user_id, response_mode="blocking",
        )
        intent_outputs = DifyClient.extract_outputs(intent_result)
        parsed_intent = intent_outputs.get("parsed_intent", "")
        intent_dict = AIService._parse_parsed_intent(parsed_intent)

        yield AIService._sse("thinking", f"解析完成：目的地 {intent_dict.get('destination', '未知')}，{intent_dict.get('days', '3')} 天")

        # Step 2: 行程生成（流式）
        async for event in generator_client.run_workflow_stream(
            inputs={"parsed_intent": parsed_intent}, user=user_id,
        ):
            event_type = event.get("event", "")
            if event_type == "workflow_started":
                yield AIService._sse("thinking", "AI 正在规划每日行程...")
            elif event_type == "node_started":
                node_title = event.get("data", {}).get("title", "")
                if node_title:
                    yield AIService._sse("thinking", f"AI 正在补充{node_title}信息...")
            elif event_type == "workflow_finished":
                outputs = DifyClient.extract_outputs(event.get("data", {}))
                itinerary_json = outputs.get("itinerary_json", "")
                if not itinerary_json:
                    yield AIService._sse("error", "行程生成失败，请重试")
                    return

                days_data = AIService._parse_itinerary_json(itinerary_json)
                if not days_data:
                    yield AIService._sse("error", "行程数据解析失败，请重试")
                    return

                destination = outputs.get("destination") or intent_dict.get("destination", "")
                total_budget = int(outputs.get("total_cost", 0))

                yield AIService._sse("thinking", f"正在保存行程数据（{len(days_data)}天，¥{total_budget}）...")

                itinerary = await ItineraryCRUDService.create_itinerary(
                    db=db, user_id=user_id,
                    title=f"AI定制行程 - {destination}",
                    destination=destination,
                    days_data=days_data,
                    start_date=date.today().isoformat(),
                    end_date=(date.today() + timedelta(days=len(days_data) - 1)).isoformat(),
                    total_budget=total_budget,
                    status="draft", source="ai_generated",
                    dify_workflow_run_id=event.get("workflow_run_id"),
                    raw_input={"query": query, "intent": intent_outputs, "generator": outputs},
                )
                yield AIService._sse("done", {"itinerary_id": itinerary["id"], "data": itinerary})
            elif event_type == "error":
                yield AIService._sse("error", "AI 生成过程出错，请重试")
                return

    # ==================== Mock 降级 ====================

    @staticmethod
    async def _generate_mock(db: AsyncSession | None, user_id: str, query: str) -> dict:
        mock = AIService._build_mock(query)
        logger.info(f"[AI] Mock 生成: destination={mock['destination']}, days={len(mock['days'])}")
        if db is None:
            return mock
        return await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id,
            title=mock["title"], destination=mock["destination"],
            days_data=mock["days"],
            start_date=mock["start_date"], end_date=mock["end_date"],
            total_budget=mock["total_budget"],
            status="draft", source="ai_generated",
            raw_input=query,
        )

    @staticmethod
    async def _generate_stream_mock(
        db: AsyncSession, user_id: str, query: str,
    ) -> AsyncGenerator[str, None]:
        steps = ["正在解析您的出行意图...", "匹配目的地 POI 数据...", "优化行程路线...", "生成每日行程安排...", "正在保存行程数据..."]
        for step in steps:
            yield AIService._sse("thinking", step)
        mock = AIService._build_mock(query)
        itinerary = await ItineraryCRUDService.create_itinerary(
            db=db, user_id=user_id,
            title=mock["title"], destination=mock["destination"],
            days_data=mock["days"],
            start_date=mock["start_date"], end_date=mock["end_date"],
            total_budget=mock["total_budget"],
            status="draft", source="ai_generated",
            raw_input=query,
        )
        yield AIService._sse("done", {"itinerary_id": itinerary["id"], "data": itinerary})

    # ==================== 解析工具 ====================

    @staticmethod
    def _parse_parsed_intent(raw: str) -> dict:
        """解析 Dify 意图解析输出的分号分隔 key=value 字符串"""
        result = {}
        if not raw:
            return result
        for part in raw.split(";"):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                k, v = k.strip(), v.strip()
                if v and v != "null" and v != "none":
                    result[k] = v
        return result

    @staticmethod
    def _parse_itinerary_json(raw: str) -> list[dict]:
        """
        解析 Dify 行程生成输出的自定义格式:

        day=1|activities=time=12:00|activity=午餐|location=XX|duration=60|price=60|type=餐厅~
            time=13:30|activity=宽窄巷子|location=XX|...~
            time=18:00|activity=晚餐|location=XX|...|hotel=酒店名|hotel_price=350|day_cost=140
        $$day=2|...

        分隔符规则:
          $$  — 分隔每天
          ~   — 分隔每个活动（出现在 type=餐厅~time=13:30 中，即 type 值末尾）
          |   — 分隔 key=value 键值对
          =   — 键值分隔

        解析策略：
          1. 按 $$ 切分每天
          2. 对每天：提取 day= N，找到 activities= 后面的内容
          3. 按 ~ 分割各活动（~ 嵌在 | 流中，如 "...|type=餐厅~time=13:30|..."）
          4. 对每个活动块按 | 再按 = 解析字段
        """
        import re
        import uuid

        if not raw:
            return []

        days = []
        day_blocks = raw.split("$$")

        for day_block in day_blocks:
            day_block = day_block.strip()
            if not day_block:
                continue

            # 提取 day=N
            day_index = 1
            m = re.search(r"day\s*=\s*(\d+)", day_block)
            if m:
                day_index = int(m.group(1))

            # 提取 hotel 信息（在 activities~... 之后，以 |hotel= 开头）
            hotel_name = ""
            hotel_price = 0
            hotel_m = re.search(r"\|\s*hotel\s*=\s*([^|]+)", day_block)
            if hotel_m:
                hotel_name = hotel_m.group(1).strip()
            hp_m = re.search(r"\|\s*hotel_price\s*=\s*(\d+)", day_block)
            if hp_m:
                hotel_price = int(hp_m.group(1))

            # 提取 activities 部分：从 activities= 开始，到 |hotel= 或字符串结尾
            # 先找到 activities= 的位置
            act_start = day_block.find("activities=")
            if act_start == -1:
                # 没有活动，跳过
                continue
            act_start += len("activities=")

            # 找到 hotel= 的位置作为 activities 结束
            hotel_pos = day_block.find("|hotel=", act_start)
            if hotel_pos == -1:
                activities_section = day_block[act_start:]
            else:
                activities_section = day_block[act_start:hotel_pos]

            # 按 ~ 分割各活动
            activity_tokens = [t.strip() for t in activities_section.split("~") if t.strip()]

            activities = []
            for token in activity_tokens:
                # 每个 token 形如: time=12:00|activity=午餐|location=XX|duration=60|price=60|type=餐厅
                # 注意：最后一个字段可能带有 ~ 残留，但上面 split 已经处理了
                fields = {}
                for f in token.split("|"):
                    f = f.strip()
                    if "=" in f:
                        k, v = f.split("=", 1)
                        fields[k.strip()] = v.strip()

                if not fields:
                    continue

                activity = {
                    "id": str(uuid.uuid4()),
                    "type": fields.get("type", "attraction"),
                    "name": fields.get("activity", ""),
                    "description": "",
                    "address": fields.get("location", ""),
                    "lat": 0.0,
                    "lng": 0.0,
                    "start_time": fields.get("time", ""),
                    "end_time": "",
                    "price": int(float(fields.get("price", 0))),
                    "duration": fields.get("duration", ""),
                    "tags": [],
                    "notes": "",
                }
                activities.append(activity)

            # 酒店
            hotel = None
            if hotel_name and hotel_name.lower() != "null" and hotel_name:
                hotel = {
                    "id": str(uuid.uuid4()),
                    "name": hotel_name,
                    "address": "",
                    "lat": 0.0,
                    "lng": 0.0,
                    "price": hotel_price,
                    "tags": [],
                }

            days.append({
                "day_index": day_index,
                "date": (date.today() + timedelta(days=day_index - 1)).isoformat(),
                "activities": activities,
                "hotel": hotel,
            })

        return days

    # ==================== 动态重排路由 ====================

    # 重排意图关键词（命中任意一个 + 有活跃行程 → 走 ReplanService）
    # 场景覆盖：天气原因（太热/太冷/下雨/下雪/台风/暴雨）、
    #          航班/交通延误/取消、身体不舒服/生病/健康原因、景点关闭等
    REPLAN_KEYWORDS = [
        # 天气相关
        "天气", "下雨", "下大雨", "暴雨", "台风", "太热", "太冷", "高温", "降温",
        "下雪", "暴晒", "恶劣天气", "天气不好", "天气原因",
        # 交通/航班相关
        "航班", "延误", "飞机", "火车晚点", "高铁", "停飞", "取消", "封路",
        # 健康/身体相关
        "身体", "不舒服", "生病", "头疼", "发烧", "感冒", "健康", "状态不好",
        "身体不适", "不太舒服",
        # 行程变更通用词
        "取消", "修改", "调整", "改", "关闭", "不行", "去不了", "变更",
        "变化", "重新安排", "重排", "换个", "替代", "替代方案", "怎么办",
        "没法去", "计划取消", "行程取消", "不想去了", "去不成了",
    ]

    @staticmethod
    def _is_replan_intent(query: str) -> bool:
        """检测用户消息是否包含动态重排意图"""
        for kw in AIService.REPLAN_KEYWORDS:
            if kw in query:
                return True
        return False

    @staticmethod
    def _extract_replan_params(query: str) -> tuple[str, dict]:
        """从用户自然语言中提取 event_type 和 event_detail

        覆盖场景：
        - 天气：太热/太冷/下大雨/暴雨/台风/下雪/高温
        - 交通：航班延误/飞机取消/火车晚点
        - 健康：身体不舒服/生病/头疼/发烧
        - 通用：取消/去不了/景点关闭
        """
        q = query.lower()
        event_type = "custom"
        event_detail: dict = {"description": query}

        # ---- 天气相关 ----
        if any(w in query for w in ["天气", "下雨", "下大雨", "暴雨", "下雪", "高温", "太热", "太冷", "降温", "暴晒", "天气不好", "天气原因"]):
            event_type = "weather_alert"
            if "雨" in query:
                event_detail = {"weather_type": "降雨", "affected_time": "明天"}
            elif any(w in query for w in ["热", "高温", "暴晒"]):
                event_detail = {"weather_type": "高温酷暑", "affected_time": "近期"}
            elif any(w in query for w in ["冷", "降温", "雪"]):
                event_detail = {"weather_type": "低温寒潮", "affected_time": "近期"}
            else:
                event_detail = {"weather_type": "异常天气", "affected_time": "近期"}

        # ---- 航班/交通延误 ----
        elif any(w in query for w in ["航班", "飞机", "延误", "停飞"]):
            event_type = "flight_delay"
            event_detail = {"delay_hours": "未知", "flight_no": "未知航班"}
            if "延误" in query:
                m = __import__("re").search(r"(\d+)\s*(小时|小时|hrs?|h)", query)
                if m:
                    event_detail["delay_hours"] = m.group(1)

        # ---- 健康/身体不适 ----
        elif any(w in query for w in ["身体", "不舒服", "生病", "头", "发烧", "感冒", "健康", "状态不好", "身体不适"]):
            event_type = "health_issue"
            event_detail = {"symptom": "身体状态不佳", "recovery_time": "待定"}

        # ---- 景点/场所关闭 ----
        elif "关闭" in query:
            event_type = "attraction_closed"
            event_detail = {"attraction_name": "相关景点/场所", "reason": query}

        return event_type, event_detail

    @staticmethod
    async def _route_replan(
        db: AsyncSession | None, user_id: str, query: str, itinerary_id: str,
    ) -> dict:
        """路由到 ReplanService 动态重排，返回带 type 标记的结果"""
        event_type, event_detail = AIService._extract_replan_params(query)
        logger.info(f"[AI] 重排参数: event_type={event_type}, detail={event_detail}")

        if db is not None:
            result = await ReplanService.replan(
                db, itinerary_id, event_type, event_detail, user_id,
            )
        else:
            # Memory mode: 返回兜底方案
            result = {
                "itinerary_id": itinerary_id,
                "event_type": event_type,
                "event_detail": event_detail,
                "event_description": query,
                "alternatives": ReplanService._fallback_alternatives(event_type),
                "workflow_run_id": None,
            }

        # 标记响应类型，前端据此区分行程 vs 重排方案
        result["type"] = "replan"
        return result

    # ==================== 工具方法 ====================

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
        """构建模拟行程 — 从 query 中智能提取目的地"""
        import re

        # 已知城市列表
        known_cities = [
            "北京", "成都", "上海", "杭州", "西安", "大理", "三亚", "云南",
            "新疆", "西藏", "桂林", "厦门", "青岛", "哈尔滨", "长沙", "重庆",
            "武汉", "南京", "苏州", "广州", "深圳", "张家界", "九寨沟", "黄山",
            "丽江", "香格里拉", "乌鲁木齐", "喀纳斯", "吐鲁番",
        ]
        destination = None
        for city in known_cities:
            if city in query:
                destination = city
                break

        # 如果没匹配到，用正则提取 "去XX" 或 "XX之旅" 中的地名
        if not destination:
            m = re.search(r"去(\w{2,4})(?:玩|旅游|旅行|之旅)?", query)
            if m:
                destination = m.group(1)
        if not destination:
            m = re.search(r"(\w{2,4})之旅", query)
            if m:
                destination = m.group(1)
        if not destination:
            destination = "默认目的地"

        # 提取天数
        days_count = 3
        m = re.search(r"(\d+)\s*天", query)
        if m:
            days_count = int(m.group(1))

        # 提取预算
        budget = 3000
        m = re.search(r"预算.*?(\d+)", query)
        if m:
            budget = int(m.group(1))
        m = re.search(r"(\d+)\s*元", query)
        if m:
            budget = int(m.group(1))

        start_date = date(2026, 7, 1)
        days = []
        for d in range(days_count):
            activities = [
                {"id": str(uuid.uuid4()), "type": "attraction",
                 "name": f"{destination}推荐景点第{d+1}天",
                 "description": f"{destination}热门打卡地",
                 "address": f"{destination}市中心", "lat": 30.0, "lng": 120.0,
                 "start_time": "09:00", "end_time": "12:00",
                 "price": 50, "tags": ["热门", "推荐"]},
                {"id": str(uuid.uuid4()), "type": "restaurant",
                 "name": f"{destination}特色餐厅",
                 "description": f"品尝地道{destination}美食",
                 "address": f"{destination}市中心", "lat": 30.0, "lng": 120.0,
                 "start_time": "12:00", "end_time": "13:30",
                 "price": 80, "tags": ["美食", "特色"]},
            ]
            hotel = {"id": str(uuid.uuid4()), "name": f"{destination}舒适酒店",
                     "address": f"{destination}市中心", "lat": 30.0, "lng": 120.0,
                     "price": 300, "tags": ["舒适", "市中心"]} if d < days_count - 1 else None
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
