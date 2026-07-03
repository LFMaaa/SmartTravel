from fastapi import APIRouter, Depends, Header, Query, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from common.schemas import APIResponse
from common.auth import decode_token
from ..database import get_db
from ..services.review_service import ReviewService

router = APIRouter()


class CreateReviewRequest(BaseModel):
    content: str
    rating: int = None
    parent_id: str = None


async def get_optional_user(x_user_token: str = Header(None)) -> str | None:
    """从 x-user-token 头解析用户 ID（可选）"""
    if not x_user_token:
        return None
    payload = decode_token(x_user_token)
    if payload and payload.type == "access":
        return payload.sub
    return None


async def get_current_user(x_user_token: str = Header(None)) -> str:
    """从 x-user-token 头解析用户 ID（必须登录）"""
    if not x_user_token:
        raise HTTPException(status_code=401, detail="请先登录")
    payload = decode_token(x_user_token)
    if not payload or payload.type != "access":
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    return payload.sub


@router.get("/poi/{poi_id}", response_model=APIResponse)
async def get_reviews(
    poi_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """获取 POI 评论列表（无需登录）"""
    result = await ReviewService.get_reviews(db, poi_id, page, page_size)
    return APIResponse(data=result)


@router.post("/poi/{poi_id}", response_model=APIResponse)
async def create_review(
    poi_id: str,
    req: CreateReviewRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """发表评论/回复（需要登录）"""
    if req.rating is not None and (req.rating < 1 or req.rating > 5):
        raise HTTPException(status_code=400, detail="评分必须在 1-5 之间")
    result = await ReviewService.create_review(
        db, poi_id, user_id, req.content, req.rating, req.parent_id
    )
    return APIResponse(data=result, message="评论发表成功")


@router.delete("/{review_id}", response_model=APIResponse)
async def delete_review(
    review_id: str,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(get_current_user),
):
    """删除评论（仅本人）"""
    await ReviewService.delete_review(db, review_id, user_id)
    return APIResponse(message="评论已删除")


@router.post("/{review_id}/like", response_model=APIResponse)
async def like_review(review_id: str, db: AsyncSession = Depends(get_db)):
    """点赞评论（无需登录）"""
    result = await ReviewService.toggle_like(db, review_id)
    return APIResponse(data=result)
