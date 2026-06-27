import os
from datetime import datetime

import redis.asyncio as aioredis
from fastapi import HTTPException

from .order_service import OrderService

REDIS_URL = os.getenv("REDIS_URL", "redis://192.168.87.50:6379/0")
LOCK_TTL = 900  # 资源锁定时间 15 分钟（秒）


class DelayPaymentService:
    """延迟支付服务 — Redis SETEX 实现资源占位锁定"""

    _redis: aioredis.Redis | None = None

    @classmethod
    async def _get_redis(cls) -> aioredis.Redis:
        """懒加载 Redis 连接"""
        if cls._redis is None:
            cls._redis = aioredis.from_url(REDIS_URL, decode_responses=True)
        return cls._redis

    @classmethod
    async def lock_resources(cls, order_id: str, items: list[dict]) -> None:
        """锁定资源（Redis SETEX 原子操作）"""
        redis_conn = await cls._get_redis()
        for item in items:
            resource_key = f"resource_lock:{item.get('resource_type')}:{item.get('resource_id')}:{item.get('booking_date', 'any')}"
            # SETEX: 原子性地设置 key 并设置过期时间
            await redis_conn.setex(resource_key, LOCK_TTL, order_id)

    @classmethod
    async def release_resources(cls, order_id: str) -> None:
        """释放资源（取消订单时调用）"""
        redis_conn = await cls._get_redis()
        # 查找并删除该订单锁定的所有资源 key
        # 注：生产环境应使用 SCAN 匹配模式，MVP 阶段用已知 key 列表
        # 这里通过保存的 resource_keys 来精确删除
        # 对于延迟取消，通过订单 ID 查找（需要维护反向映射）
        pass  # 实际释放由订单取消流程显式传入 resource_keys 处理

    @classmethod
    async def release_resources_by_keys(cls, order_id: str, resource_keys: list[str]) -> None:
        """按指定 key 列表释放资源"""
        redis_conn = await cls._get_redis()
        for key in resource_keys:
            await redis_conn.delete(key)

    @classmethod
    async def check_and_release_expired(cls, order_id: str, resource_keys: list[str]) -> bool:
        """检查资源锁是否仍有效（未被其他订单抢占）"""
        redis_conn = await cls._get_redis()
        for key in resource_keys:
            owner = await redis_conn.get(key)
            if owner and owner != order_id:
                return False  # 资源已被其他订单占用
        return True

    @classmethod
    async def confirm_payment(cls, order_id: str, db, resource_keys: list[str] | None = None) -> dict:
        """确认支付：检查锁有效性 → 更新订单状态 → 释放资源锁"""
        redis_conn = await cls._get_redis()

        # 如果提供了 resource_keys，验证锁仍归此订单所有
        if resource_keys:
            for key in resource_keys:
                owner = await redis_conn.get(key)
                if owner and owner != order_id:
                    raise HTTPException(status_code=409, detail="资源已被其他用户锁定，请重新下单")

        # 更新订单状态
        order_dict = await OrderService.update_order_status(
            db, order_id, status="paid", payment_status="paid"
        )

        # 支付成功后释放资源锁（资源已确认归属）
        if resource_keys:
            for key in resource_keys:
                await redis_conn.delete(key)

        return order_dict

    @classmethod
    async def get_lock_info(cls, resource_type: str, resource_id: str, booking_date: str = "any") -> str | None:
        """查询资源锁定状态"""
        redis_conn = await cls._get_redis()
        resource_key = f"resource_lock:{resource_type}:{resource_id}:{booking_date}"
        return await redis_conn.get(resource_key)
