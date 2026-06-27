"""
会员支付 API — 支付宝沙箱支付
- POST /payment/member/create       — 创建会员支付订单，返回支付宝支付链接
- POST /payment/member/alipay-notify — 支付宝异步通知回调
- GET  /payment/member/status/{order_id} — 查询支付状态
"""

import json
import logging
import uuid
from datetime import datetime, timedelta
from decimal import Decimal

from fastapi import APIRouter, Depends, Request, HTTPException, Query
from fastapi.responses import PlainTextResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..models.order import Order, OrderItem
from ..services.order_service import OrderService
from ..services.alipay_service import build_pay_url, verify_notify

logger = logging.getLogger("smarttravel.payment.member")

router = APIRouter()

# 会员价格
MEMBER_PRICE = 99.00


@router.post("/member/create")
async def create_member_order(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    创建 Pro 会员支付订单

    请求体:
      { "user_id": "xxx" }

    返回:
      {
        "order_id": "xxx",
        "total_amount": 99.00,
        "alipay_url": "https://openapi.alipaydev.com/gateway.do?...",  // 支付宝支付链接，未配置时为 null
        "sandbox_mode": true  // 沙箱模式提示
      }
    """
    try:
        body = await request.json()
    except Exception:
        body = {}
    user_id = body.get("user_id", "")

    if not user_id:
        raise HTTPException(status_code=400, detail="缺少 user_id")

    order_id = str(uuid.uuid4())
    expire_at = datetime.utcnow() + timedelta(minutes=30)

    # 创建订单
    order = Order(
        id=order_id,
        user_id=user_id,
        total_amount=Decimal(str(MEMBER_PRICE)),
        status="pending",
        payment_status="unpaid",
        expire_at=expire_at,
    )
    db.add(order)

    # 创建订单项
    item = OrderItem(
        order_id=order_id,
        resource_type="hotel",  # 复用枚举值，实际为"会员"
        resource_id="pro_membership",
        resource_name="Pro 会员年费",
        unit_price=Decimal(str(MEMBER_PRICE)),
        quantity=1,
    )
    db.add(item)
    await db.flush()

    # 生成支付宝支付链接
    alipay_url = build_pay_url(
        out_trade_no=order_id,
        total_amount=MEMBER_PRICE,
        subject="智游 Pro 会员年费",
        body="解锁全部智能旅行功能：无限行程生成、动态实时重规划、深度定制推荐等",
    )

    logger.info(f"[会员支付] 订单创建: {order_id}, 用户: {user_id}, 支付宝链接: {'已生成' if alipay_url else '未配置'}")

    return {
        "code": 0,
        "data": {
            "order_id": order_id,
            "total_amount": MEMBER_PRICE,
            "alipay_url": alipay_url,
            "sandbox_mode": alipay_url is None,
        },
        "message": "订单创建成功",
    }


@router.post("/member/alipay-notify")
async def alipay_notify(request: Request, db: AsyncSession = Depends(get_db)):
    """
    支付宝异步通知回调

    支付宝支付成功后，同步通知商户系统
    商户需要验证签名，确认后处理订单状态升级
    """
    form_data = await request.form()
    params = dict(form_data)
    logger.info(f"[支付宝通知] 收到回调: trade_no={params.get('trade_no')}, out_trade_no={params.get('out_trade_no')}, status={params.get('trade_status')}")

    trade_status = params.get("trade_status", "")
    out_trade_no = params.get("out_trade_no", "")
    total_amount = params.get("total_amount", "")

    # 验证签名
    if not verify_notify(dict(params)):
        logger.warning("[支付宝通知] 签名验证失败")
        return PlainTextResponse("fail")

    # 只处理 TRADE_SUCCESS 状态
    if trade_status not in ("TRADE_SUCCESS", "TRADE_FINISHED"):
        logger.info(f"[支付宝通知] 交易状态非成功: {trade_status}")
        return PlainTextResponse("success")

    # 查询订单
    result = await db.execute(select(Order).where(Order.id == out_trade_no))
    order = result.scalar_one_or_none()

    if not order:
        logger.warning(f"[支付宝通知] 订单不存在: {out_trade_no}")
        return PlainTextResponse("fail")

    if order.status == "paid":
        logger.info(f"[支付宝通知] 订单已处理: {out_trade_no}")
        return PlainTextResponse("success")

    # 更新订单状态
    order.status = "paid"
    order.payment_status = "paid"
    order.paid_at = datetime.utcnow()
    await db.flush()

    logger.info(f"[支付宝通知] 支付成功: 订单={out_trade_no}, 金额={total_amount}, 用户={order.user_id}")

    # 调用 user-service 升级会员
    await _upgrade_member(order.user_id)

    return PlainTextResponse("success")


@router.get("/member/status/{order_id}")
async def get_member_pay_status(order_id: str, db: AsyncSession = Depends(get_db)):
    """
    查询会员支付状态

    GET /payment/member/status/{order_id}

    返回:
      {
        "order_id": "xxx",
        "status": "paid" | "pending" | "timeout",
        "paid_at": "..."
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


@router.post("/member/sandbox-pay/{order_id}")
async def sandbox_pay_member(
    order_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """
    沙箱模拟支付（开发环境用，直接标记订单已支付并升级会员）
    """
    # 查询订单
    result = await db.execute(select(Order).where(Order.id == order_id))
    order = result.scalar_one_or_none()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    if order.status == "paid":
        logger.info(f"[沙箱支付] 订单已支付: {order_id}")
        return {"code": 0, "message": "订单已支付"}

    # 标记支付成功
    order.status = "paid"
    order.payment_status = "paid"
    order.paid_at = datetime.utcnow()
    await db.flush()

    logger.info(f"[沙箱支付] 模拟支付成功: 订单={order_id}, 用户={order.user_id}")

    # 升级会员
    await _upgrade_member(order.user_id)

    return {
        "code": 0,
        "data": {
            "order_id": order_id,
            "status": "paid",
            "is_pro": True,
        },
        "message": "支付成功，已升级为 Pro 会员",
    }


async def _upgrade_member(user_id: str):
    """
    调用 user-service 升级用户为 Pro 会员
    """
    import os
    try:
        import httpx
        user_service_url = os.getenv(
            "USER_SERVICE_URL", "http://user-service:8001"
        )
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(
                f"{user_service_url}/api/v1/user/upgrade-member",
                json={"user_id": user_id},
            )
            if resp.status_code == 200:
                logger.info(f"[会员升级] 用户 {user_id} 已升级为 Pro 会员")
            else:
                logger.warning(f"[会员升级] 升级失败: {resp.status_code} {resp.text}")
    except Exception as e:
        logger.error(f"[会员升级] 调用 user-service 失败: {e}")
