"""
Dify 工作流 API 客户端

串联3个工作流：
1. 意图解析 (IntentParser) — 自然语言 → 结构化参数
2. 行程生成 (ItineraryGenerator) — 结构化参数 → 完整行程 JSON
3. 动态重排 (ReplanAgent) — 行程 + 事件 → 备选方案
"""
import json
import os
import logging
from typing import AsyncGenerator, Optional

import httpx

logger = logging.getLogger(__name__)

# ============================================================
# 工作流 API Key 配置
# ============================================================
DIFY_BASE_URL = os.getenv("DIFY_BASE_URL", "http://192.168.87.50:80")

DIFY_INTENT_PARSER_KEY = os.getenv(
    "DIFY_INTENT_PARSER_KEY",
    "app-2XOCKXdJkSyBsLeR7o8JTG30",
)
DIFY_ITINERARY_GENERATOR_KEY = os.getenv(
    "DIFY_ITINERARY_GENERATOR_KEY",
    "app-2ccAvTt3JVl7UmMATtDF9Dbe",
)
DIFY_REPLAN_AGENT_KEY = os.getenv(
    "DIFY_REPLAN_AGENT_KEY",
    "app-RNaSnptlWqcYQNt4zsm0JV3F",
)


class DifyClient:
    """Dify 工作流 API 客户端（同步 + 流式）"""

    def __init__(self, api_key: str, base_url: str = DIFY_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                timeout=httpx.Timeout(120.0, connect=10.0),
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
        return self._client

    async def close(self):
        if self._client:
            await self._client.aclose()
            self._client = None

    async def run_workflow(
        self,
        inputs: dict,
        user: str = "smarttravel-user",
        response_mode: str = "blocking",
    ) -> dict:
        """同步运行工作流，等待完整结果返回"""
        client = await self._get_client()
        payload = {
            "inputs": inputs,
            "response_mode": response_mode,
            "user": user,
        }
        logger.info(f"[Dify] run_workflow → {self.base_url}/v1/workflows/run, inputs={json.dumps(inputs, ensure_ascii=False)[:200]}")
        response = await client.post("/v1/workflows/run", json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(f"[Dify] workflow completed: workflow_run_id={data.get('workflow_run_id')}")
        return data

    async def run_workflow_stream(
        self,
        inputs: dict,
        user: str = "smarttravel-user",
    ) -> AsyncGenerator[dict, None]:
        """流式运行工作流，实时产出 SSE 事件"""
        client = await self._get_client()
        payload = {
            "inputs": inputs,
            "response_mode": "streaming",
            "user": user,
        }
        logger.info(f"[Dify] run_workflow_stream → {self.base_url}/v1/workflows/run, inputs={json.dumps(inputs, ensure_ascii=False)[:200]}")
        async with client.stream("POST", "/v1/workflows/run", json=payload) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if not line or not line.startswith("data: "):
                    continue
                try:
                    event = json.loads(line[6:])
                    yield event
                except json.JSONDecodeError:
                    logger.warning(f"[Dify] failed to parse SSE line: {line[:100]}")
                    continue

    @staticmethod
    def extract_outputs(data: dict) -> dict:
        inner = data.get("data", data)
        outputs = inner.get("outputs", {})
        if not outputs:
            outputs = data.get("outputs", {})
        return outputs

    @staticmethod
    def extract_text_output(data: dict, key: str = "text") -> str:
        outputs = DifyClient.extract_outputs(data)
        return str(outputs.get(key, outputs.get("result", "")))

    @staticmethod
    def extract_json_output(data: dict, key: str = "json") -> dict:
        outputs = DifyClient.extract_outputs(data)
        raw = outputs.get(key, outputs.get("result", "{}"))
        if isinstance(raw, dict):
            return raw
        if isinstance(raw, str):
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                logger.warning(f"[Dify] failed to parse JSON output: {raw[:200]}")
                return {}
        return {}


# ============================================================
# 三个工作流客户端（单例模式）
# ============================================================

_intent_client: Optional[DifyClient] = None
_generator_client: Optional[DifyClient] = None
_replan_client: Optional[DifyClient] = None
_dify_available: bool | None = None
_dify_checked_at: float = 0.0
_DIFY_HEALTH_TTL: float = 60.0  # 健康检查缓存有效期（秒）


async def check_dify_health(force_retry: bool = False) -> bool:
    """检测 Dify 是否可达（通过尝试调用意图解析工作流）

    结果会缓存 _DIFY_HEALTH_TTL 秒，避免每次请求都检测。
    当首次调用失败后，后续调用会按指数退避重试（最多 5 分钟）。
    """
    global _dify_available, _dify_checked_at, _DIFY_HEALTH_TTL
    import time

    now = time.time()
    if _dify_available is not None and not force_retry:
        elapsed = now - _dify_checked_at
        if elapsed < _DIFY_HEALTH_TTL:
            return _dify_available
        # 缓存过期，重新检查

    try:
        client = get_intent_client()
        c = await client._get_client()
        resp = await c.get("/v1/workflows/run", timeout=httpx.Timeout(5.0, connect=3.0))
        _dify_available = resp.status_code in (200, 400, 401, 404, 405)
    except Exception:
        _dify_available = False

    _dify_checked_at = now
    # 如果检查失败，缩短下次重试间隔；成功则使用正常 TTL
    if not _dify_available:
        _DIFY_HEALTH_TTL = min(_DIFY_HEALTH_TTL * 2, 300.0)  # 指数退避，最长 5 分钟
    else:
        _DIFY_HEALTH_TTL = 60.0  # 成功后恢复正常 1 分钟缓存

    logger.info(f"[Dify] 健康检查: {'可用' if _dify_available else '不可用'} ({DIFY_BASE_URL}), TTL={_DIFY_HEALTH_TTL:.0f}s")
    return _dify_available


def is_dify_available() -> bool:
    return _dify_available is True


def get_intent_client() -> DifyClient:
    global _intent_client
    if _intent_client is None:
        _intent_client = DifyClient(api_key=DIFY_INTENT_PARSER_KEY)
    return _intent_client


def get_generator_client() -> DifyClient:
    global _generator_client
    if _generator_client is None:
        _generator_client = DifyClient(api_key=DIFY_ITINERARY_GENERATOR_KEY)
    return _generator_client


def get_replan_client() -> DifyClient:
    global _replan_client
    if _replan_client is None:
        _replan_client = DifyClient(api_key=DIFY_REPLAN_AGENT_KEY)
    return _replan_client
