"""
预订支付 API — 支付宝沙箱支付（行程资源预订）
- POST /payment/booking/create          — 创建预订支付订单，返回支付宝支付链接
- POST /payment/booking/sandbox-pay/{order_id} — 沙箱模拟支付（开发环境）
- GET  /payment/booking/status/{order_id}      — 查询支付状态
"""

import logging
import uuid
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, List

from fastapi import APIRouter, Depends, Request, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.order import Order, OrderItem
from ..services.alipay_service import build_pay_url

logger = logging.getLogger("smarttravel.payment.booking")

router = APIRouter()


class BookingItemSchema(BaseModel):
    resource_type: str = "hotel"
    resource_id: Optional[str] = None
    resource_name: str = ""
    unit_price: float = 0.0
    quantity: int = 1


class BookingOrderSchema(BaseModel):
    user_id: str
    itinerary_id: Optional[str] = None
    total_amount: float
    items: List[BookingItemSchema]
    return_url: Optional[str] = None


@router.post("/booking/create")
async def create_booking_order(
    body: BookingOrderSchema,
    db: AsyncSession = Depends(get_db),
):
    """
    创建预订支付订单

    请求体:
      {
        "user_id": "xxx",
        "itinerary_id": "xxx",       // 可选：关联行程
        "total_amount": 2310.00,
        "items": [
          { "resource_type": "hotel", "resource_id": "h1", "resource_name": "希尔顿", "unit_price": 1280, "quantity": 1 },
          ...
        ],
        "return_url": "http://localhost:5173/itinerary/payment?paid=1"  // 支付完成后跳转地址
      }

    返回:
      {
        "code": 0,
        "data": {
          "order_id": "xxx",
          "total_amount": 2310.00,
          "alipay_url": "https://openapi.alipaydev.com/gateway.do?...",
          "sandbox_mode": false
        },
        "message": "订单创建成功"
      }
    """
    user_id = body.user_id
    itinerary_id = body.itinerary_id
    total_amount = body.total_amount
    items = body.items
    return_url = body.return_url

    if not user_id:
        raise HTTPException(status_code=400, detail="缺少 user_id")
    if not items or total_amount <= 0:
        raise HTTPException(status_code=400, detail="缺少 items 或 total_amount 无效")

    order_id = str(uuid.uuid4())
    expire_at = datetime.utcnow() + timedelta(minutes=30)

    # 创建订单
    order = Order(
        id=order_id,
        user_id=user_id,
        itinerary_id=itinerary_id,
        total_amount=Decimal(str(total_amount)),
        status="pending",
        payment_status="unpaid",
        expire_at=expire_at,
    )
    db.add(order)

    # 创建订单项
    for item_data in items:
        item = OrderItem(
            order_id=order_id,
            resource_type=item_data.resource_type,
            resource_id=item_data.resource_id or "",
            resource_name=item_data.resource_name,
            unit_price=Decimal(str(item_data.unit_price)),
            quantity=item_data.quantity,
        )
        db.add(item)

    await db.flush()

    # 生成支付宝支付链接
    alipay_url = build_pay_url(
        out_trade_no=order_id,
        total_amount=total_amount,
        subject="智慧旅游行程预订",
        body=f"预订酒店、门票、餐饮等 {len(items)} 项服务",
        return_url=return_url,
    )

    logger.info(f"[预订支付] 订单创建: {order_id}, 用户: {user_id}, 金额: {total_amount}, 项目数: {len(items)}, 支付宝: {'已生成' if alipay_url else '未配置'}")

    return {
        "code": 0,
        "data": {
            "order_id": order_id,
            "total_amount": total_amount,
            "alipay_url": alipay_url,
            "sandbox_mode": alipay_url is None,
        },
        "message": "预订订单创建成功",
    }


@router.get("/booking/status/{order_id}")
async def get_booking_pay_status(order_id: str, db: AsyncSession = Depends(get_db)):
    """
    查询预订支付状态

    GET /payment/booking/status/{order_id}

    返回:
      {
        "code": 0,
        "data": {
          "order_id": "xxx",
          "status": "paid" | "pending" | "timeout",
          "paid_at": "..." | null
        }
      }
    """
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    return {
        "code": 0,
        "data": {
            "order_id": order.id,
            "status": order.status,
            "paid_at": order.paid_at.isoformat() if order.paid_at else None,
        },
    }


@router.post("/booking/sandbox-pay/{order_id}")
async def sandbox_pay_booking(
    order_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    沙箱模拟支付（开发环境用，直接标记订单已支付）
    """
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status == "paid":
        logger.info(f"[沙箱支付-预订] 订单已支付: {order_id}")
        return {"code": 0, "message": "订单已支付"}

    # 标记支付成功
    order.status = "paid"
    order.payment_status = "paid"
    order.paid_at = datetime.utcnow()
    await db.flush()

    logger.info(f"[沙箱支付-预订] 模拟支付成功: 订单={order_id}, 金额={order.total_amount}, 用户={order.user_id}")

    return {
        "code": 0,
        "data": {
            "order_id": order_id,
            "status": "paid",
        },
        "message": "支付成功，预订已完成",
    }
