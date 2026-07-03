import uuid
import logging
from datetime import datetime
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException

logger = logging.getLogger(__name__)

# 直接用 raw SQL 操作，避免额外定义 ORM model


class ReviewService:

    @staticmethod
    async def get_reviews(db: AsyncSession, poi_id: str, page: int = 1, page_size: int = 20) -> dict:
        """获取 POI 评论列表（一级评论 + 嵌套回复），按时间倒序"""
        from sqlalchemy import text

        # 总数
        total_sql = text("SELECT COUNT(*) as cnt FROM poi_reviews WHERE poi_id = :poi_id AND parent_id IS NULL")
        total_result = await db.execute(total_sql, {"poi_id": poi_id})
        total = total_result.scalar() or 0

        # 平均评分
        avg_sql = text("SELECT AVG(rating) as avg_r FROM poi_reviews WHERE poi_id = :poi_id AND parent_id IS NULL AND rating IS NOT NULL")
        avg_result = await db.execute(avg_sql, {"poi_id": poi_id})
        avg_rating = round(float(avg_result.scalar() or 0), 1)

        # 一级评论
        offset = (page - 1) * page_size
        reviews_sql = text("""
            SELECT r.id, r.poi_id, r.user_id, r.parent_id, r.content, r.rating, r.likes, r.created_at,
                   u.nickname as user_name, u.avatar_url as user_avatar
            FROM poi_reviews r
            LEFT JOIN users u ON r.user_id = u.id
            WHERE r.poi_id = :poi_id AND r.parent_id IS NULL
            ORDER BY r.created_at DESC
            LIMIT :limit OFFSET :offset
        """)
        reviews_result = await db.execute(reviews_sql, {"poi_id": poi_id, "limit": page_size, "offset": offset})
        reviews = reviews_result.mappings().all()

        # 回复
        items = []
        for r in reviews:
            replies_sql = text("""
                SELECT r2.id, r2.poi_id, r2.user_id, r2.parent_id, r2.content, r2.likes, r2.created_at,
                       u.nickname as user_name, u.avatar_url as user_avatar
                FROM poi_reviews r2
                LEFT JOIN users u ON r2.user_id = u.id
                WHERE r2.parent_id = :parent_id
                ORDER BY r2.created_at ASC
            """)
            replies_result = await db.execute(replies_sql, {"parent_id": r.id})
            replies = replies_result.mappings().all()

            items.append({
                "id": r.id,
                "poi_id": r.poi_id,
                "user_id": r.user_id,
                "user_name": r.user_name or "匿名用户",
                "user_avatar": r.user_avatar,
                "content": r.content,
                "rating": r.rating,
                "likes": r.likes or 0,
                "created_at": r.created_at.isoformat() if r.created_at else "",
                "replies": [{
                    "id": rp.id,
                    "user_id": rp.user_id,
                    "user_name": rp.user_name or "匿名用户",
                    "user_avatar": rp.user_avatar,
                    "content": rp.content,
                    "likes": rp.likes or 0,
                    "created_at": rp.created_at.isoformat() if rp.created_at else "",
                    "reply_to": r.user_name or "匿名用户",
                } for rp in replies],
            })

        return {"items": items, "total": total, "avg_rating": avg_rating, "page": page, "page_size": page_size}

    @staticmethod
    async def create_review(db: AsyncSession, poi_id: str, user_id: str, content: str,
                            rating: int = None, parent_id: str = None) -> dict:
        """发表评论或回复"""
        from sqlalchemy import text

        if not content or not content.strip():
            raise HTTPException(status_code=400, detail="评论内容不能为空")

        # 如果是回复，检查父评论存在
        if parent_id:
            check_sql = text("SELECT id FROM poi_reviews WHERE id = :id")
            check_result = await db.execute(check_sql, {"id": parent_id})
            if not check_result.scalar():
                raise HTTPException(status_code=404, detail="父评论不存在")

        review_id = str(uuid.uuid4())
        insert_sql = text("""
            INSERT INTO poi_reviews (id, poi_id, user_id, parent_id, content, rating, likes, created_at)
            VALUES (:id, :poi_id, :user_id, :parent_id, :content, :rating, 0, :created_at)
        """)
        await db.execute(insert_sql, {
            "id": review_id,
            "poi_id": poi_id,
            "user_id": user_id,
            "parent_id": parent_id,
            "content": content.strip(),
            "rating": rating if parent_id is None else None,
            "created_at": datetime.utcnow(),
        })

        # 查用户昵称
        user_sql = text("SELECT nickname, avatar_url FROM users WHERE id = :uid")
        user_result = await db.execute(user_sql, {"uid": user_id})
        user_row = user_result.mappings().first()
        user_name = user_row["nickname"] if user_row else "匿名用户"

        return {
            "id": review_id,
            "poi_id": poi_id,
            "user_id": user_id,
            "user_name": user_name,
            "parent_id": parent_id,
            "content": content.strip(),
            "rating": rating if parent_id is None else None,
            "likes": 0,
            "created_at": datetime.utcnow().isoformat(),
        }

    @staticmethod
    async def delete_review(db: AsyncSession, review_id: str, user_id: str):
        """删除评论（仅本人可删除）"""
        from sqlalchemy import text

        check_sql = text("SELECT user_id FROM poi_reviews WHERE id = :id")
        result = await db.execute(check_sql, {"id": review_id})
        row = result.mappings().first()
        if not row:
            raise HTTPException(status_code=404, detail="评论不存在")
        if row["user_id"] != user_id:
            raise HTTPException(status_code=403, detail="只能删除自己的评论")

        delete_sql = text("DELETE FROM poi_reviews WHERE id = :id")
        await db.execute(delete_sql, {"id": review_id})

    @staticmethod
    async def toggle_like(db: AsyncSession, review_id: str) -> dict:
        """点赞（+1），再次调用取消（-1）— 简化版，实际应记录点赞用户"""
        from sqlalchemy import text

        update_sql = text("UPDATE poi_reviews SET likes = likes + 1 WHERE id = :id")
        await db.execute(update_sql, {"id": review_id})

        get_sql = text("SELECT likes FROM poi_reviews WHERE id = :id")
        result = await db.execute(get_sql, {"id": review_id})
        likes = result.scalar() or 0

        return {"likes": likes}
