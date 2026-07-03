"""
意图解析 — 自然语言 → 结构化参数

输入: "带父母去北京5天，预算1.5万，喜欢历史文化，腿脚不好不爬山"
输出: { destination: "北京", days: 5, budget: 15000, style: "历史文化",
         companion: "家庭", constraints: "不爬山" }
"""
import json
import logging
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from .llm_service import get_llm

logger = logging.getLogger(__name__)

INTENT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", """你是一个专业的旅行意图解析助手。从用户输入中提取以下信息，输出严格的 JSON 格式：

{{
  "destination": "目的地城市（中文）",
  "days": 天数(数字),
  "budget": 预算金额(数字，单位元),
  "style": "旅行风格（如历史文化/美食/自然风光/都市购物/休闲度假等）",
  "companion": "同行人（如家庭/朋友/独自/情侣/亲子等）",
  "constraints": "特殊限制（如不爬山/不走太多路/需要无障碍设施等，无则为空字符串）"
}}

规则:
- 如果某个字段用户没有提到，destination 设为 "未指定"，days 设为 3，budget 设为 3000，其他字段设为空字符串
- 只输出 JSON，不要有任何其他文字
- 目的地必须是中文城市名"""),
    ("human", "{query}"),
])

INTENT_OUTPUT_PARSER = StrOutputParser()


async def parse_intent(query: str) -> dict:
    """解析用户自然语言 → 结构化旅行参数"""
    llm = get_llm(temperature=0.1)
    chain = INTENT_PROMPT | llm | INTENT_OUTPUT_PARSER

    result = await chain.ainvoke({"query": query})
    result = result.strip()

    # 清理 markdown 代码块
    if result.startswith("```"):
        result = result.split("```")[1]
        if result.startswith("json"):
            result = result[4:]
        result = result.strip()

    try:
        intent = json.loads(result)
    except json.JSONDecodeError:
        logger.warning(f"[IntentParser] JSON 解析失败: {result[:200]}")
        intent = _fallback_parse(query)

    logger.info(f"[IntentParser] {query[:50]} → {intent}")
    return intent


def _fallback_parse(query: str) -> dict:
    """JSON 解析失败时的降级方案：正则提取"""
    import re
    result = {"destination": "未指定", "days": 3, "budget": 3000, "style": "", "companion": "", "constraints": ""}

    # 提取天数
    m = re.search(r"(\d+)\s*天", query)
    if m:
        result["days"] = int(m.group(1))

    # 提取预算
    m = re.search(r"预算.*?(\d+)", query)
    if m:
        val = int(m.group(1))
        result["budget"] = val if val > 100 else val * 10000  # "1.5万" → 15000

    # 提取目的地
    cities = ["北京", "成都", "上海", "杭州", "西安", "大理", "三亚", "云南",
              "新疆", "西藏", "桂林", "厦门", "青岛", "哈尔滨", "长沙", "重庆",
              "武汉", "南京", "苏州", "广州", "深圳", "丽江", "昆明", "贵阳"]
    for city in cities:
        if city in query:
            result["destination"] = city
            break

    # 提取风格
    if any(w in query for w in ["文化", "历史", "古"]):
        result["style"] = "历史文化"
    elif any(w in query for w in ["美食", "吃"]):
        result["style"] = "美食"
    elif any(w in query for w in ["自然", "风景", "发呆", "拍照"]):
        result["style"] = "自然风光"

    # 同行人
    if any(w in query for w in ["爸妈", "父母", "家庭", "带父母", "带孩子"]):
        result["companion"] = "家庭"
    elif any(w in query for w in ["朋友", "闺蜜"]):
        result["companion"] = "朋友"
    elif any(w in query for w in ["一个人", "独自", "自己"]):
        result["companion"] = "独自"
    elif any(w in query for w in ["情侣", "蜜月", "女朋友", "男朋友"]):
        result["companion"] = "情侣"

    # 限制条件
    if any(w in query for w in ["不爬山", "不走太多路", "腿脚不好", "不方便"]):
        result["constraints"] = "不爬山，减少步行"

    return result
