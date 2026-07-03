"""
LangChain LLM 服务层 — DeepSeek V3

架构:
  LLM (deepseek-chat)
    ├── IntentParser: 自然语言 → 结构化参数
    ├── ItineraryGenerator: 参数 + POI Tool → 完整行程 JSON
    └── ReplanAgent: 当前行程 + 事件 → 多套备选方案

配置:
  DEEPSEEK_API_KEY  — DeepSeek API Key
  DEEPSEEK_BASE_URL — 默认 https://api.deepseek.com/v1
"""
import os
import logging
from typing import Optional

from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)

# ============================================================
# LLM 单例
# ============================================================
_llm: Optional[ChatOpenAI] = None
_llm_available: bool | None = None


def get_llm(temperature: float = 0.3, max_tokens: int = 4096) -> ChatOpenAI:
    """获取 DeepSeek V3 LLM 实例"""
    global _llm
    if _llm is None:
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

        if not api_key:
            logger.warning("[LLM] DEEPSEEK_API_KEY 未配置，LLM 不可用")
            raise RuntimeError("DEEPSEEK_API_KEY 未配置")

        _llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=120,
            max_retries=2,
        )
        logger.info(f"[LLM] DeepSeek V3 已连接: {base_url}")
    return _llm


async def check_llm_health(force: bool = False) -> bool:
    """检测 LLM 是否可用"""
    global _llm_available
    if _llm_available is not None and not force:
        return _llm_available

    try:
        llm = get_llm()
        await llm.ainvoke("ping")
        _llm_available = True
    except Exception as e:
        logger.warning(f"[LLM] 健康检查失败: {e}")
        _llm_available = False

    return _llm_available


def is_llm_available() -> bool:
    return _llm_available is True
