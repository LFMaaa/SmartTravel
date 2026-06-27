import uuid
import logging
from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.order import Order, OrderItem

logger = logging.getLogger("smarttravel.payment")

# 尝试导入 MQ 发布器
try:
    from common.mq import MQClient, RK_ORDER_CREATED, RK_ORDER_PAID, RK_ORDER_TIMEOUT
    MQ_AVAILABLE = True
except ImportError:
    MQ_AVAILABLE = False


class OrderService:
    """订单服务 — MySQL 持久化 + MQ 事件发布"""

    @staticmethod
    async def create_order(db: AsyncSession, order_data: dict) -> dict:
        """创建订单（含延迟支付占位）"""
        order_id = str(uuid.uuid4())
        expire_at = datetime.utcnow() + timedelta(minutes=15)

        order = Order(
            id=order_id,
            user_id=order_data.get("user_id", ""),
            itinerary_id=order_data.get("itinerary_id"),
            total_amount=Decimal(str(order_data.get("total_amount", 0))),
            status="pending",
            payment_status="unpaid",
            expire_at=expire_at,
        )
        db.add(order)

        # 创建订单项
        for item_data in order_data.get("items", []):
            item = OrderItem(
                order_id=order_id,
                resource_type=item_data.get("resource_type", "hotel"),
                resource_id=item_data.get("resource_id", ""),
                resource_name=item_data.get("resource_name", ""),
                unit_price=Decimal(str(item_data.get("unit_price", 0))),
                quantity=item_data.get("quantity", 1),
                booking_date=item_data.get("booking_date"),
                check_in=item_data.get("check_in"),
                check_out=item_data.get("check_out"),
            )
            db.add(item)

        await db.flush()

        # 发布订单创建事件
        if MQ_AVAILABLE:
            try:
                await MQClient.publish(RK_ORDER_CREATED, {
                    "event_type": "order_created",
                    "order_id": order_id,
                    "user_id": order.user_id,
                    "total_amount": float(order.total_amount),
                    "expire_at": expire_at.isoformat(),
                    "created_at": order.created_at.isoformat() if order.created_at else None,
                })
            except Exception as e:
                logger.warning(f"MQ 发布失败（非致命）: {e}")

        return {
            "id": order_id,
            "user_id": order.user_id,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "expire_at": expire_at.isoformat(),
            "created_at": order.created_at.isoformat() if order.created_at else None,
        }

    @staticmethod
    async def get_order(db: AsyncSession, order_id: str) -> dict:
        """查询订单详情"""
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        return OrderService._order_to_dict(order)

    @staticmethod
    async def list_orders(db: AsyncSession, user_id: str, page: int, page_size: int) -> dict:
        """获取用户订单列表（分页）"""
        count_result = await db.execute(
            select(func.count(Order.id)).where(Order.user_id == user_id)
        )
        total = count_result.scalar() or 0

        offset = (page - 1) * page_size
        result = await db.execute(
            select(Order)
            .where(Order.user_id == user_id)
            .order_by(Order.created_at.desc())
            .offset(offset)
            .limit(page_size)
        )
        orders = result.scalars().all()

        return {
            "items": [OrderService._order_to_dict(o) for o in orders],
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    @staticmethod
    async def update_order_status(
        db: AsyncSession, order_id: str, status: str, payment_status: str | None = None
    ) -> dict:
        """更新订单状态 + 发布 MQ 事件"""
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")

        order.status = status
        if payment_status:
            order.payment_status = payment_status
        if status == "paid":
            order.paid_at = datetime.utcnow()
        if status == "timeout":
            order.payment_status = "unpaid"

        await db.flush()
        order_dict = OrderService._order_to_dict(order)

        # 发布 MQ 事件
        if MQ_AVAILABLE:
            routing_key = {
                "paid": RK_ORDER_PAID,
                "timeout": RK_ORDER_TIMEOUT,
                "cancelled": RK_ORDER_TIMEOUT,
            }.get(status)

            if routing_key:
                try:
                    await MQClient.publish(routing_key, {
                        "event_type": f"order_{status}",
                        "order_id": order_id,
                        "user_id": order.user_id,
                        "total_amount": float(order.total_amount),
                        "status": status,
                    })
                except Exception as e:
                    logger.warning(f"MQ 发布失败（非致命）: {e}")

        return order_dict

    @staticmethod
    async def get_expired_pending_orders(db: AsyncSession) -> list[Order]:
        """获取已过期的待支付订单（用于定时任务批量取消）"""
        result = await db.execute(
            select(Order).where(
                Order.status == "pending",
                Order.expire_at < datetime.utcnow(),
            )
        )
        return list(result.scalars().all())

    @staticmethod
    def _order_to_dict(order: Order) -> dict:
        return {
            "id": order.id,
            "user_id": order.user_id,
            "itinerary_id": order.itinerary_id,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "payment_status": order.payment_status,
            "expire_at": order.expire_at.isoformat() if order.expire_at else None,
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
            "created_at": order.created_at.isoformat() if order.created_at else None,
            "items": [
                {
                    "id": item.id,
                    "resource_type": item.resource_type,
                    "resource_id": item.resource_id,
                    "resource_name": item.resource_name,
                    "unit_price": float(item.unit_price),
                    "quantity": item.quantity,
                    "booking_date": item.booking_date.isoformat() if item.booking_date else None,
                    "check_in": item.check_in.isoformat() if item.check_in else None,
                    "check_out": item.check_out.isoformat() if item.check_out else None,
                }
                for item in (order.items or [])
            ],
        }
