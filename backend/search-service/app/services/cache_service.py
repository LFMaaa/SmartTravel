import os
import json
from typing import Optional

import redis.asyncio as aioredis

REDIS_URL = os.getenv("REDIS_URL", "redis://192.168.87.50:6379/0")
CACHE_TTL = 300  # 缓存 5 分钟


class CacheService:
    """Redis 缓存服务 — 用于搜索结果缓存"""

    _redis: aioredis.Redis | None = None

    @classmethod
    async def _get_redis(cls) -> aioredis.Redis:
        """懒加载 Redis 连接"""
        if cls._redis is None:
            try:
                cls._redis = aioredis.from_url(REDIS_URL, decode_responses=True)
            except Exception:
                # Redis 不可用时返回 None，降级为无缓存模式
                return None
        return cls._redis

    @classmethod
    def _build_key(cls, prefix: str, **params) -> str:
        """构建缓存 key"""
        sorted_params = sorted(params.items())
        param_str = ":".join(f"{k}={v}" for k, v in sorted_params if v)
        return f"smarttravel:{prefix}:{param_str}"

    @classmethod
    async def get(cls, prefix: str, **params) -> Optional[dict]:
        """从缓存获取数据"""
        try:
            redis_conn = await cls._get_redis()
            if redis_conn is None:
                return None
            key = cls._build_key(prefix, **params)
            cached = await redis_conn.get(key)
            if cached:
                return json.loads(cached)
        except Exception:
            pass
        return None

    @classmethod
    async def set(cls, prefix: str, data: dict, **params) -> None:
        """写入缓存"""
        try:
            redis_conn = await cls._get_redis()
            if redis_conn is None:
                return
            key = cls._build_key(prefix, **params)
            await redis_conn.setex(key, CACHE_TTL, json.dumps(data, ensure_ascii=False))
        except Exception:
            pass  # 缓存写入失败不影响主流程

    @classmethod
    async def invalidate(cls, prefix: str) -> None:
        """使缓存失效（按前缀批量删除）"""
        try:
            redis_conn = await cls._get_redis()
            if redis_conn is None:
                return
            pattern = f"smarttravel:{prefix}:*"
            keys = await redis_conn.keys(pattern)
            if keys:
                await redis_conn.delete(*keys)
        except Exception:
            pass
