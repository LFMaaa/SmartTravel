import os
import json
from typing import Optional

from elasticsearch import AsyncElasticsearch

from ..es.mappings import POI_INDEX_MAPPING

ES_HOST = os.getenv("ES_HOST", "192.168.87.50")
ES_PORT = int(os.getenv("ES_PORT", "9200"))
POI_INDEX = "poi"


class ESService:
    """Elasticsearch 搜索服务 — 支持全文/地理/补全/筛选"""

    _client: AsyncElasticsearch | None = None

    @classmethod
    async def _get_client(cls) -> AsyncElasticsearch:
        if cls._client is None:
            cls._client = AsyncElasticsearch(
                hosts=[f"http://{ES_HOST}:{ES_PORT}"],
                verify_certs=False,
            )
        return cls._client

    @classmethod
    async def ensure_index(cls) -> None:
        """确保 POI 索引存在，不存在则创建"""
        client = await cls._get_client()
        exists = await client.indices.exists(index=POI_INDEX)
        if not exists:
            await client.indices.create(index=POI_INDEX, body=POI_INDEX_MAPPING)

    @classmethod
    async def index_poi(cls, poi_data: dict) -> str:
        """索引单个 POI 文档"""
        client = await cls._get_client()
        doc_id = poi_data.pop("poi_id", poi_data.pop("id", None))
        result = await client.index(
            index=POI_INDEX, id=doc_id, body=poi_data, refresh=True,
        )
        return result["_id"]

    @classmethod
    async def bulk_index_pois(cls, pois: list[dict]) -> int:
        """批量索引 POI 文档"""
        client = await cls._get_client()
        operations = []
        for poi in pois:
            doc_id = poi.pop("poi_id", poi.pop("id", None))
            operations.append({"index": {"_index": POI_INDEX, "_id": doc_id}})
            operations.append(poi)
        if operations:
            result = await client.bulk(operations=operations, refresh=True)
            return len(result.get("items", [])) if not result.get("errors") else 0
        return 0

    # ==================== 全文搜索 ====================

    @classmethod
    async def search_poi(
        cls,
        keyword: str,
        city: str = "",
        poi_type: str = "",
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """多维度 POI 全文搜索

        支持: 关键词匹配(name^3, description^2, tags)、城市筛选、类型筛选
        排序: popularity_score desc + _score
        """
        client = await cls._get_client()
        try:
            await cls.ensure_index()
        except Exception:
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

        must = []
        if keyword:
            must.append({
                "multi_match": {
                    "query": keyword,
                    "fields": ["name^3", "description^2", "tags^1.5", "address"],
                    "type": "best_fields",
                    "fuzziness": "AUTO",
                }
            })

        filters = []
        if city:
            filters.append({"term": {"city": city}})
        if poi_type:
            filters.append({"term": {"type": poi_type}})

        body = {
            "query": {
                "bool": {
                    "must": must if must else [{"match_all": {}}],
                    "filter": filters,
                }
            },
            "from": (page - 1) * page_size,
            "size": page_size,
            "sort": [
                {"popularity_score": {"order": "desc"}},
                "_score",
            ],
        }

        try:
            result = await client.search(index=POI_INDEX, body=body)
            hits = result["hits"]["hits"]
            items = [cls._hit_to_poi(h) for h in hits]
            total = result["hits"]["total"]["value"] if isinstance(result["hits"]["total"], dict) else result["hits"]["total"]
            return {"items": items, "total": total, "page": page, "page_size": page_size}
        except Exception:
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

    # ==================== 地理位置搜索 ====================

    @classmethod
    async def search_nearby(
        cls,
        lat: float,
        lng: float,
        radius: int = 3000,
        poi_type: str = "",
        page: int = 1,
        page_size: int = 10,
    ) -> dict:
        """地理位置搜索（附近 POI）

        按距离升序排列，支持类型筛选
        """
        try:
            await cls.ensure_index()
        except Exception:
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

        client = await cls._get_client()

        filters = [{
            "geo_distance": {
                "distance": f"{radius}m",
                "location": {"lat": lat, "lon": lng},
            }
        }]
        if poi_type:
            filters.append({"term": {"type": poi_type}})

        body = {
            "query": {"bool": {"filter": filters}},
            "from": (page - 1) * page_size,
            "size": page_size,
            "sort": [{
                "_geo_distance": {
                    "location": {"lat": lat, "lon": lng},
                    "order": "asc",
                    "unit": "m",
                }
            }],
        }

        try:
            result = await client.search(index=POI_INDEX, body=body)
            hits = result["hits"]["hits"]
            items = [
                {**cls._hit_to_poi(h), "distance": f"{h.get('sort', [0])[0]:.0f}m" if h.get("sort") else None}
                for h in hits
            ]
            total = result["hits"]["total"]["value"] if isinstance(result["hits"]["total"], dict) else result["hits"]["total"]
            return {"items": items, "total": total, "page": page, "page_size": page_size}
        except Exception:
            return {"items": [], "total": 0, "page": page, "page_size": page_size}

    # ==================== 自动补全 ====================

    @classmethod
    async def suggest(cls, keyword: str, size: int = 5) -> list[str]:
        """搜索自动补全

        优先使用 name_suggest completion 字段，
        ES 不支持时降级为 match_phrase_prefix
        """
        try:
            await cls.ensure_index()
        except Exception:
            return cls._mock_suggest(keyword, size)

        client = await cls._get_client()

        # 优先使用 completion suggest
        try:
            result = await client.search(
                index=POI_INDEX,
                body={
                    "suggest": {
                        "poi_suggest": {
                            "prefix": keyword,
                            "completion": {"field": "name_suggest", "size": size},
                        }
                    },
                    "_source": ["name"],
                },
            )
            options = result.get("suggest", {}).get("poi_suggest", [{}])[0].get("options", [])
            if options:
                return [o["_source"]["name"] for o in options]
        except Exception:
            pass

        # 降级: match_phrase_prefix
        try:
            result = await client.search(
                index=POI_INDEX,
                body={
                    "query": {
                        "match_phrase_prefix": {
                            "name": {"query": keyword, "max_expansions": 10},
                        }
                    },
                    "size": size,
                    "_source": ["name"],
                },
            )
            return [h["_source"]["name"] for h in result["hits"]["hits"]]
        except Exception:
            return cls._mock_suggest(keyword, size)

    # ==================== 工具方法 ====================

    @classmethod
    def _hit_to_poi(cls, hit: dict) -> dict:
        """ES hit → 前端 POI 格式"""
        src = hit["_source"]
        loc = src.get("location", {})
        return {
            "id": hit["_id"],
            "name": src.get("name", ""),
            "type": src.get("type", ""),
            "city": src.get("city", ""),
            "district": src.get("district", ""),
            "rating": src.get("rating", 0),
            "price": src.get("price", 0),
            "tags": src.get("tags", []),
            "lat": loc.get("lat"),
            "lng": loc.get("lon"),
            "address": src.get("address", ""),
            "description": src.get("description", ""),
            "opening_hours": src.get("opening_hours", ""),
            "popularity_score": src.get("popularity_score", 0),
        }

    @classmethod
    def _mock_suggest(cls, keyword: str, size: int) -> list[str]:
        """模拟降级补全（ES 不可用时使用）"""
        mock_data = {
            "北京": ["故宫博物院", "天坛公园", "颐和园", "八达岭长城", "鸟巢"],
            "成都": ["成都大熊猫基地", "宽窄巷子", "武侯祠", "锦里古街", "杜甫草堂"],
            "上海": ["外滩", "上海迪士尼乐园", "豫园", "南京路步行街", "东方明珠"],
            "西安": ["兵马俑", "西安城墙", "回民街", "大雁塔", "华清池"],
            "三亚": ["亚龙湾", "天涯海角", "蜈支洲岛", "南山寺", "海棠湾"],
            "云南": ["大理古城", "丽江古城", "玉龙雪山", "洱海", "香格里拉"],
        }
        for city, names in mock_data.items():
            if city in keyword:
                return names[:size]
        # Generic fallback
        matches = []
        for names in mock_data.values():
            for name in names:
                if keyword in name:
                    matches.append(name)
        return matches[:size] if matches else [f"{keyword}热门推荐{i+1}" for i in range(min(size, 5))]
