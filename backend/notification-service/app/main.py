from contextlib import asynccontextmanager
import asyncio
import logging

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from .api.routes import router as notification_router
from .database import init_db
from .services.push_service import PushService

logger = logging.getLogger("smarttravel.notification")

# 尝试导入 MQ 模块
try:
    from common.mq import MQClient, QUEUE_NOTIFICATION, RK_ORDER_CREATED, RK_ORDER_PAID, RK_ORDER_TIMEOUT, RK_REPLAN_GENERATED, RK_WEATHER_ALERT
    MQ_AVAILABLE = True
except ImportError:
    logger.warning("common.mq 模块不可用，消息队列功能将禁用")
    MQ_AVAILABLE = False


async def handle_order_event(message: dict):
    """处理订单相关事件 → 推送通知给用户"""
    user_id = message.get("user_id")
    event_type = message.get("event_type", "")
    if event_type == "order_created":
        await PushService.send_to_user(user_id, {
            "type": "payment_reminder",
            "title": "订单已创建",
            "content": f"您的订单 {message.get('order_id', '')} 已创建，请在15分钟内完成支付。",
            "resource_type": "order",
            "resource_id": message.get("order_id"),
        })
    elif event_type == "order_paid":
        await PushService.send_to_user(user_id, {
            "type": "payment_reminder",
            "title": "支付成功",
            "content": f"订单 {message.get('order_id', '')} 已支付成功。",
            "resource_type": "order",
            "resource_id": message.get("order_id"),
        })
    elif event_type == "order_timeout":
        await PushService.send_to_user(user_id, {
            "type": "payment_reminder",
            "title": "订单已超时取消",
            "content": f"订单 {message.get('order_id', '')} 未在规定时间内支付，已自动取消。",
            "resource_type": "order",
            "resource_id": message.get("order_id"),
        })


async def handle_replan_event(message: dict):
    """处理重排事件 → 推送备选方案给用户"""
    user_id = message.get("user_id")
    itinerary_id = message.get("itinerary_id")
    event_type = message.get("event_type", "replan")
    alternative_count = len(message.get("alternatives", []))

    await PushService.send_to_user(user_id, {
        "type": "replan_alert",
        "title": f"行程 {itinerary_id[:8]}... 受到 {event_type} 影响",
        "content": f"已生成 {alternative_count} 套备选方案供您选择。",
        "resource_type": "itinerary",
        "resource_id": itinerary_id,
    })


async def handle_weather_alert(message: dict):
    """处理天气预警 → 推送提醒"""
    user_id = message.get("user_id")
    await PushService.send_to_user(user_id, {
        "type": "system",
        "title": "天气预警",
        "content": message.get("alert_text", "您的目的地有天气变化，请注意出行安全。"),
        "resource_type": "weather",
    })


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时创建数据库表 + 启动 MQ 消费"""
    await init_db()

    # 启动 RabbitMQ 消费者（后台任务）
    if MQ_AVAILABLE:
        try:
            # 延迟启动确保 RabbitMQ 就绪
            await asyncio.sleep(5)
            await MQClient.start_consumer(
                queue_name=QUEUE_NOTIFICATION,
                routing_keys=[RK_ORDER_CREATED, RK_ORDER_PAID, RK_ORDER_TIMEOUT],
                callback=handle_order_event,
            )
            await MQClient.start_consumer(
                queue_name=QUEUE_NOTIFICATION,
                routing_keys=[RK_REPLAN_GENERATED],
                callback=handle_replan_event,
            )
            await MQClient.start_consumer(
                queue_name=QUEUE_NOTIFICATION,
                routing_keys=[RK_WEATHER_ALERT],
                callback=handle_weather_alert,
            )
            logger.info("Notification Service MQ 消费者已启动")
        except Exception as e:
            logger.warning(f"MQ 消费者启动失败（非致命）: {e}")

    yield

    # 关闭 MQ 连接
    if MQ_AVAILABLE:
        try:
            await MQClient.close()
        except Exception:
            pass


app = FastAPI(
    title="SmartTravel Notification Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(notification_router, prefix="/api/v1/notification")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "notification-service"}
