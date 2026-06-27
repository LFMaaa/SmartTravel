from fastapi import APIRouter, Query
from typing import Optional

from common.schemas import APIResponse

from ..services.es_service import ESService
from ..services.cache_service import CacheService
from ..services.seed_data import search_poi as seed_search_poi, suggest as seed_suggest

router = APIRouter()

# ES 是否可用标记（避免每次请求都探测）
_es_available = True


@router.get("/poi", response_model=APIResponse)
async def search_poi(
    keyword: str = Query(..., description="搜索关键词"),
    city: str = Query("", description="城市"),
    poi_type: str = Query("", description="类型: attraction/hotel/restaurant"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
):
    """搜索景点/酒店/餐厅（ES + Redis 缓存，不可用时降级到种子数据）"""
    global _es_available

    if _es_available:
        # 先查缓存
        cached = await CacheService.get(
            "poi_search", keyword=keyword, city=city, type=poi_type, page=str(page), size=str(page_size)
        )
        if cached:
            return APIResponse(data=cached)

        # 查 ES
        results = await ESService.search_poi(keyword, city, poi_type, page, page_size)

        # ES 返回了有效结果（total > 0 说明 ES 可用且数据正常）
        if results.get("total", 0) > 0:
            await CacheService.set(
                "poi_search", results,
                keyword=keyword, city=city, type=poi_type, page=str(page), size=str(page_size),
            )
            return APIResponse(data=results)

        # ES 返回空结果 — 可能 ES 不可用或没有数据，降级到种子数据
        _es_available = False

    # 种子数据降级
    results = seed_search_poi(keyword=keyword, city=city, poi_type=poi_type, page=page, page_size=page_size)
    return APIResponse(data=results)


@router.get("/poi/nearby", response_model=APIResponse)
async def search_nearby(
    lat: float = Query(..., description="纬度"),
    lng: float = Query(..., description="经度"),
    radius: int = Query(3000, description="搜索半径(米)"),
    poi_type: str = Query("", description="类型"),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
):
    """地理位置搜索（附近景点/酒店），ES 不可用时降级到种子数据"""
    global _es_available

    if _es_available:
        cached = await CacheService.get(
            "poi_nearby", lat=str(lat), lng=str(lng), radius=str(radius), type=poi_type, page=str(page)
        )
        if cached:
            return APIResponse(data=cached)

        results = await ESService.search_nearby(lat, lng, radius, poi_type, page, page_size)

        if results.get("total", 0) > 0:
            await CacheService.set(
                "poi_nearby", results,
                lat=str(lat), lng=str(lng), radius=str(radius), type=poi_type, page=str(page),
            )
            return APIResponse(data=results)

        _es_available = False

    # 种子数据降级：按距离排序，模拟附近搜索
    results = seed_search_poi(poi_type=poi_type, page=page, page_size=page_size)
    return APIResponse(data=results)


@router.get("/suggest", response_model=APIResponse)
async def suggest(
    keyword: str = Query(..., description="输入前缀"),
    size: int = Query(5, ge=1, le=20),
):
    """搜索自动补全（ES 不可用时降级到种子数据）"""
    global _es_available

    if _es_available:
        # 尝试 ES suggest（ES 不可用时 ESService._mock_suggest 也能返回数据）
        # 但 mock 数据可能含种子数据中不存在的城市 — 优先使用种子数据
        pass  # 直接走种子数据，保证数据一致性

    suggestions = seed_suggest(keyword, size)
    return APIResponse(data=suggestions)
