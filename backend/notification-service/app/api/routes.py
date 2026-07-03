from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from pydantic import BaseModel

from common.schemas import APIResponse

from ..services.push_service import PushService

router = APIRouter()


class PushNotificationRequest(BaseModel):
    user_id: str
    type: str
    title: str
    content: dict
    resource_type: str = ""
    resource_id: str = ""


@router.post("/push", response_model=APIResponse)
async def push_notification(req: PushNotificationRequest):
    """HTTP 推送通知（天气监控等服务调用）"""
    notification = await PushService.send_to_user(
        user_id=req.user_id,
        message={
            "type": req.type,
            "title": req.title,
            "content": req.content,
            "resource_type": req.resource_type,
            "resource_id": req.resource_id,
        },
    )
    return APIResponse(data=notification, message="通知已发送")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    """WebSocket 连接（实时推送通知）"""
    await PushService.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 处理客户端消息（如心跳 pong）
            if data == "ping":
                await websocket.send_text("pong")
    except WebSocketDisconnect:
        PushService.disconnect(user_id)
    except Exception:
        PushService.disconnect(user_id)


@router.get("/notifications", response_model=APIResponse)
async def get_notifications(
    user_id: str = Query(..., description="用户ID"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
):
    """获取通知历史（从 MySQL 查询）"""
    notifications = await PushService.get_history(user_id, page, page_size)
    return APIResponse(data=notifications)


@router.post("/notifications/{notification_id}/read", response_model=APIResponse)
async def mark_as_read(notification_id: str, user_id: str = Query(...)):
    """标记通知为已读"""
    success = await PushService.mark_as_read(user_id, notification_id)
    if not success:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="通知不存在")
    return APIResponse(message="已标记为已读")


@router.get("/notifications/unread-count", response_model=APIResponse)
async def unread_count(user_id: str = Query(..., description="用户ID")):
    """获取未读通知数"""
    count = await PushService.get_unread_count(user_id)
    return APIResponse(data={"count": count})
