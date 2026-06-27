from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from common.schemas import APIResponse

from ..database import get_db
from ..services.order_service import OrderService
from ..services.delay_payment_service import DelayPaymentService

router = APIRouter()


@router.post("/orders", response_model=APIResponse)
async def create_order(order_data: dict, db: AsyncSession = Depends(get_db)):
    """创建订单（延迟支付占位）"""
    # 获取资源锁 key 列表
    resource_keys = [
        f"resource_lock:{item.get('resource_type')}:{item.get('resource_id')}:{item.get('booking_date', 'any')}"
        for item in order_data.get("items", [])
    ]

    # 创建订单
    order = await OrderService.create_order(db, order_data)

    # Redis 锁定资源
    try:
        await DelayPaymentService.lock_resources(order["id"], order_data.get("items", []))
    except Exception:
        # 资源锁定失败，取消订单
        await OrderService.update_order_status(db, order["id"], "cancelled")
        from fastapi import HTTPException
        raise HTTPException(status_code=409, detail="资源已被锁定，请稍后重试")

    return APIResponse(data={**order, "resource_keys": resource_keys})


@router.get("/orders/{order_id}", response_model=APIResponse)
async def get_order(order_id: str, db: AsyncSession = Depends(get_db)):
    """查询订单状态"""
    order = await OrderService.get_order(db, order_id)
    return APIResponse(data=order)


@router.post("/orders/{order_id}/pay", response_model=APIResponse)
async def pay_order(order_id: str, pay_data: dict | None = None, db: AsyncSession = Depends(get_db)):
    """确认支付"""
    resource_keys = pay_data.get("resource_keys", []) if pay_data else []
    result = await DelayPaymentService.confirm_payment(order_id, db, resource_keys)
    return APIResponse(data=result)


@router.post("/orders/{order_id}/cancel", response_model=APIResponse)
async def cancel_order(order_id: str, cancel_data: dict | None = None, db: AsyncSession = Depends(get_db)):
    """取消订单（释放占位资源）"""
    resource_keys = cancel_data.get("resource_keys", []) if cancel_data else []
    if resource_keys:
        await DelayPaymentService.release_resources_by_keys(order_id, resource_keys)
    await OrderService.update_order_status(db, order_id, "cancelled")
    return APIResponse(message="订单已取消，资源已释放")


@router.get("/orders", response_model=APIResponse)
async def list_orders(
    user_id: str = Query(..., description="用户ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """获取用户订单列表"""
    orders = await OrderService.list_orders(db, user_id, page, page_size)
    return APIResponse(data=orders)
