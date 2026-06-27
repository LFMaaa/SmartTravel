import json
import uuid
from datetime import datetime

from fastapi import WebSocket
from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import async_session_factory
from ..models.notification import Notification


class PushService:
    """消息推送服务 — WebSocket 管理 + MySQL 持久化通知历史"""

    _connections: dict[str, WebSocket] = {}  # user_id -> websocket（连接对象不可序列化，仍需内存管理）

    # ==================== WebSocket 连接管理 ====================

    @classmethod
    async def connect(cls, user_id: str, websocket: WebSocket):
        await websocket.accept()
        cls._connections[user_id] = websocket

    @classmethod
    def disconnect(cls, user_id: str):
        cls._connections.pop(user_id, None)

    @classmethod
    def is_connected(cls, user_id: str) -> bool:
        return user_id in cls._connections

    # ==================== 消息推送 + 持久化 ====================

    @classmethod
    async def send_to_user(cls, user_id: str, message: dict):
        """向指定用户推送消息并持久化到 MySQL"""
        # 1. 持久化通知到 MySQL
        notification = await cls._save_notification(user_id, message)

        # 2. 如果用户在线，通过 WebSocket 实时推送
        ws = cls._connections.get(user_id)
        if ws:
            try:
                push_data = {
                    "id": notification["id"],
                    "type": message.get("type", "system"),
                    "title": message.get("title", ""),
                    "content": message.get("content", ""),
                    "resource_type": message.get("resource_type"),
                    "resource_id": message.get("resource_id"),
                    "created_at": notification["created_at"],
                }
                await ws.send_text(json.dumps(push_data, ensure_ascii=False))
            except Exception:
                # WebSocket 发送失败，连接可能已断开
                cls._connections.pop(user_id, None)

    @classmethod
    async def broadcast(cls, user_ids: list[str], message: dict):
        """向多个用户广播消息"""
        for uid in user_ids:
            await cls.send_to_user(uid, message)

    # ==================== 通知历史查询（MySQL） ====================

    @classmethod
    async def get_history(cls, user_id: str, page: int = 1, page_size: int = 10) -> dict:
        """从 MySQL 查询通知历史（分页）"""
        async with async_session_factory() as db:
            # 计数
            count_result = await db.execute(
                select(func.count(Notification.id)).where(Notification.user_id == user_id)
            )
            total = count_result.scalar() or 0

            # 分页查询
            offset = (page - 1) * page_size
            result = await db.execute(
                select(Notification)
                .where(Notification.user_id == user_id)
                .order_by(Notification.created_at.desc())
                .offset(offset)
                .limit(page_size)
            )
            notifications = result.scalars().all()

            return {
                "items": [
                    {
                        "id": n.id,
                        "type": n.type,
                        "title": n.title,
                        "content": n.content,
                        "is_read": n.is_read,
                        "resource_type": n.resource_type,
                        "resource_id": n.resource_id,
                        "created_at": n.created_at.isoformat() if n.created_at else None,
                    }
                    for n in notifications
                ],
                "total": total,
                "page": page,
                "page_size": page_size,
            }

    @classmethod
    async def mark_as_read(cls, user_id: str, notification_id: str) -> bool:
        """标记通知为已读"""
        async with async_session_factory() as db:
            result = await db.execute(
                update(Notification)
                .where(Notification.id == notification_id, Notification.user_id == user_id)
                .values(is_read=True)
            )
            await db.commit()
            return result.rowcount > 0

    @classmethod
    async def get_unread_count(cls, user_id: str) -> int:
        """获取未读通知数"""
        async with async_session_factory() as db:
            result = await db.execute(
                select(func.count(Notification.id)).where(
                    Notification.user_id == user_id,
                    Notification.is_read == False,  # noqa: E712
                )
            )
            return result.scalar() or 0

    # ==================== 内部方法 ====================

    @classmethod
    async def _save_notification(cls, user_id: str, message: dict) -> dict:
        """持久化通知到 MySQL"""
        notification = Notification(
            id=str(uuid.uuid4()),
            user_id=user_id,
            type=message.get("type", "system"),
            title=message.get("title", ""),
            content=message.get("content", ""),
            resource_type=message.get("resource_type"),
            resource_id=message.get("resource_id"),
            is_read=False,
        )
        async with async_session_factory() as db:
            db.add(notification)
            await db.commit()
            return {
                "id": notification.id,
                "created_at": notification.created_at.isoformat() if notification.created_at else None,
            }
