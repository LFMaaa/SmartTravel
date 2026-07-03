"""
行程生成器 — LangChain Agent + POI Tool Calling

流程:
  意图解析结果 + POI 搜索工具 → LLM Agent → 完整行程 JSON

输出格式:
  {
    "destination": "北京",
    "days": [
      {
        "day_index": 1,
        "date": "2026-07-01",
        "activities": [
          { "type": "attraction", "name": "故宫", "address": "...", "start_time": "09:00",
            "duration": "120分钟", "price": 60, "tags": ["历史文化"], "ai_reason": "..." }
        ],
        "hotel": { "name": "...", "price": 350 }
      }
    ],
    "total_budget": 15000
  }
"""
import json
import logging
import httpx
from typing import Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.tools import tool

from .llm_service import get_llm

logger = logging.getLogger(__name__)

# ============================================================
# POI 搜索工具 (Tool Calling) — 高德地图 POI API
# ============================================================
# 高德 POI 类型编码: https://lbs.amap.com/api/webservice/download
AMAP_POI_TYPES = {
    "attraction": "110000|120000|140000",  # 风景名胜|公园|文物古迹
    "restaurant": "050000",                 # 餐饮
    "hotel": "060000|060100|060200|060300",  # 住宿|酒店|青旅|民宿
}


@tool
async def search_poi(keyword: str, city: str = "", poi_type: str = "") -> str:
    """搜索景点、酒店或餐厅。参数: keyword(关键词), city(城市), poi_type(attraction/hotel/restaurant)。
    用于查找行程中需要的具体地点信息。调用高德地图 POI 搜索 API，返回 JSON 格式的搜索结果。"""
    import os

    api_key = os.getenv("AMAP_API_KEY", "").strip()
    if not api_key:
        logger.warning("[Tool:search_poi] AMAP_API_KEY 未配置")
        return _fallback_poi_search(keyword, city, poi_type)

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            params = {
                "key": api_key,
                "keywords": keyword,
                "offset": 5,
                "page": 1,
            }
            if city:
                params["city"] = city
            if poi_type and poi_type in AMAP_POI_TYPES:
                params["types"] = AMAP_POI_TYPES[poi_type]

            resp = await client.get(
                "https://restapi.amap.com/v3/place/text",
                params=params,
            )
            resp.raise_for_status()
            data = resp.json()

            if data.get("status") != "1":
                logger.warning(f"[Tool:search_poi] 高德 POI API 返回异常: {data.get('info')}")
                return _fallback_poi_search(keyword, city, poi_type)

            pois = data.get("pois", [])
            if not pois:
                return f"在 {city or '目标城市'} 未找到 '{keyword}' 的搜索结果"

            results = []
            for p in pois[:5]:
                # 高德返回的 biz_ext 可能包含价格信息
                biz_ext = p.get("biz_ext", {}) or {}
                results.append({
                    "name": p.get("name", ""),
                    "type": p.get("type", ""),
                    "city": p.get("cityname", city),
                    "address": p.get("address", ""),
                    "location": p.get("location", ""),
                    "tel": p.get("tel", ""),
                    "rating": p.get("biz_ext", {}).get("rating", "") if isinstance(p.get("biz_ext"), dict) else "",
                    "photos": [photo.get("url", "") for photo in (p.get("photos", []) or [])[:2]],
                })
            return json.dumps(results, ensure_ascii=False)

    except Exception as e:
        logger.warning(f"[Tool:search_poi] 高德 API 调用失败: {e}")
        return _fallback_poi_search(keyword, city, poi_type)


def _fallback_poi_search(keyword: str, city: str = "", poi_type: str = "") -> str:
    """高德 API 不可用时的降级方案：返回提示信息让 LLM 自行补全"""
    return json.dumps([{
        "name": f"{keyword}（推荐）",
        "type": poi_type or "attraction",
        "city": city or "目的地",
        "address": f"{city}市中心" if city else "目的地市中心",
        "note": "具体信息请根据常识补充",
    }], ensure_ascii=False)


# ============================================================
# 行程生成 Prompt
# ============================================================
ITINERARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的旅行规划师。根据用户的旅行参数和 POI 搜索结果，生成详细的每日行程。

输出严格的 JSON 格式（不要 markdown 代码块）:

{{
  "destination": "目的地城市",
  "days": [
    {{
      "day_index": 1,
      "date": "YYYY-MM-DD（从今天开始）",
      "weather_note": "该季节天气提示（如7月北京炎热注意防暑）",
      "activities": [
        {{
          "type": "attraction|restaurant|hotel|transport",
          "name": "活动名称",
          "address": "地址",
          "start_time": "HH:MM",
          "duration": "预计时长（如120分钟）",
          "price": 预估费用(数字),
          "tags": ["标签1", "标签2"],
          "ai_reason": "AI 推荐理由"
        }}
      ],
      "hotel": {{ "name": "推荐酒店", "address": "地址", "price": 价格 }}
    }}
  ],
  "total_budget": 总预算(数字),
  "tips": "旅行小贴士"
}}

规则:
- 每天 3-5 个活动，包含景点、餐厅、交通
- 合理安排时间（上午景点 → 午餐 → 下午景点 → 晚餐 → 酒店）
- 用 search_poi 工具搜索真实 POI 数据填充行程
- 如果有 constraints（如不爬山），避免安排此类活动
- 预算合理分配（住宿约占总预算 30-40%）
- 直接输出 JSON，不要有其他文字"""),
    ("human", """旅行参数:
- 目的地: {destination}
- 天数: {days}天
- 预算: ¥{budget}
- 风格: {style}
- 同行人: {companion}
- 特殊要求: {constraints}

已搜索到的真实 POI 数据供参考:

景点:
{poi_attractions}

酒店:
{poi_hotels}

餐厅:
{poi_restaurants}

请基于以上真实数据生成完整行程 JSON。"""),
])

ITINERARY_OUTPUT_PARSER = StrOutputParser()


async def generate_itinerary(intent: dict) -> dict:
    """根据意图参数生成完整行程

    流程:
      1. 调用 search_poi 工具获取目的地真实 POI 数据
      2. 将 POI 数据 + 意图参数传给 LLM 生成行程 JSON
    """
    llm = get_llm(temperature=0.4, max_tokens=8192)
    dest = intent.get("destination", "未指定")

    # Step 1: 调用 search_poi 获取真实数据
    poi_data = {}
    try:
        attractions = await search_poi.ainvoke({"keyword": f"{dest}景点", "city": dest, "poi_type": "attraction"})
        hotels = await search_poi.ainvoke({"keyword": f"{dest}酒店", "city": dest, "poi_type": "hotel"})
        restaurants = await search_poi.ainvoke({"keyword": f"{dest}美食", "city": dest, "poi_type": "restaurant"})
        poi_data = {
            "attractions": attractions,
            "hotels": hotels,
            "restaurants": restaurants,
        }
        logger.info(f"[ItineraryGen] POI 搜索完成: {dest}")
    except Exception as e:
        logger.warning(f"[ItineraryGen] POI 搜索失败: {e}，LLM 将自行补全")

    # Step 2: 用 LLM 生成行程
    chain = ITINERARY_PROMPT | llm | ITINERARY_OUTPUT_PARSER

    result = await chain.ainvoke({
        "destination": dest,
        "days": str(intent.get("days", 3)),
        "budget": str(intent.get("budget", 3000)),
        "style": intent.get("style", ""),
        "companion": intent.get("companion", ""),
        "constraints": intent.get("constraints", ""),
        "poi_attractions": poi_data.get("attractions", "未搜索到"),
        "poi_hotels": poi_data.get("hotels", "未搜索到"),
        "poi_restaurants": poi_data.get("restaurants", "未搜索到"),
    })

    result = result.strip()
    if result.startswith("```"):
        parts = result.split("```")
        result = parts[1]
        if result.startswith("json"):
            result = result[4:]
        result = result.strip()

    try:
        itinerary = json.loads(result)
    except json.JSONDecodeError:
        logger.warning(f"[ItineraryGen] JSON 解析失败: {result[:300]}")
        itinerary = _generate_fallback(intent)

    # 补充日期
    from datetime import date, timedelta
    start = date.today()
    for day in itinerary.get("days", []):
        idx = day.get("day_index", 1)
        day["date"] = (start + timedelta(days=idx - 1)).isoformat()

    logger.info(f"[ItineraryGen] 生成完成: {len(itinerary.get('days', []))}天, ¥{itinerary.get('total_budget', 0)}")
    return itinerary


def _generate_fallback(intent: dict) -> dict:
    """降级方案：从意图参数生成简单行程"""
    import uuid
    from datetime import date, timedelta

    dest = intent.get("destination", "推荐目的地")
    days_count = intent.get("days", 3)
    budget = intent.get("budget", 3000)
    per_day = budget // days_count

    days = []
    for d in range(days_count):
        activities = [
            {"type": "attraction", "name": f"{dest}热门景点", "address": f"{dest}市中心",
             "start_time": "09:00", "duration": "120分钟", "price": per_day // 4, "tags": ["推荐"],
             "ai_reason": f"{dest}必打卡景点"},
            {"type": "restaurant", "name": f"{dest}特色餐厅", "address": f"{dest}市中心",
             "start_time": "12:00", "duration": "60分钟", "price": per_day // 5, "tags": ["美食"],
             "ai_reason": "品尝当地特色美食"},
            {"type": "attraction", "name": f"{dest}文化地标", "address": f"{dest}市中心",
             "start_time": "14:00", "duration": "90分钟", "price": per_day // 5, "tags": ["文化"],
             "ai_reason": "了解当地文化"},
        ]
        hotel = {"name": f"{dest}舒适酒店", "address": f"{dest}市中心", "price": per_day // 3}
        days.append({
            "day_index": d + 1,
            "date": (date.today() + timedelta(days=d)).isoformat(),
            "activities": activities,
            "hotel": hotel,
        })

    return {
        "destination": dest,
        "days": days,
        "total_budget": budget,
        "tips": "此行程为降级方案，POI 搜索暂时不可用",
    }
