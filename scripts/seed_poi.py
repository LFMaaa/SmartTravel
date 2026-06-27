"""
POI 种子数据脚本
将北京、成都、上海三城的景点/酒店/餐厅基础数据写入 MySQL poi 表并同步到 Elasticsearch。
运行方式: python scripts/seed_poi.py
"""
import uuid
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

# ============================================================
# POI 种子数据（北京 / 成都 / 上海）
# ============================================================
POI_DATA = [
    # ========== 北京 ==========
    # 景点
    {"id": str(uuid.uuid4()), "name": "故宫博物院", "type": "attraction", "city": "北京", "district": "东城区",
     "address": "北京市东城区景山前街4号", "latitude": 39.9163, "longitude": 116.3972,
     "price_range": {"min": 40, "max": 60}, "rating": 4.8, "tags": ["历史文化", "世界遗产", "博物馆"],
     "description": "明清两代的皇家宫殿，中国最大的古代文化艺术博物馆，世界文化遗产。", "opening_hours": "08:30-17:00",
     "popularity_score": 98.5},
    {"id": str(uuid.uuid4()), "name": "天安门广场", "type": "attraction", "city": "北京", "district": "东城区",
     "address": "北京市东城区长安街", "latitude": 39.9087, "longitude": 116.3975,
     "price_range": {"min": 0, "max": 0}, "rating": 4.7, "tags": ["地标", "免费", "必打卡"],
     "description": "世界上最大的城市中心广场，中国国家象征。", "opening_hours": "全天",
     "popularity_score": 97.0},
    {"id": str(uuid.uuid4()), "name": "颐和园", "type": "attraction", "city": "北京", "district": "海淀区",
     "address": "北京市海淀区新建宫门路19号", "latitude": 39.9999, "longitude": 116.2755,
     "price_range": {"min": 20, "max": 30}, "rating": 4.7, "tags": ["园林", "世界遗产", "皇家"],
     "description": "中国现存最大的皇家园林，被誉为皇家园林博物馆。", "opening_hours": "06:30-18:00",
     "popularity_score": 95.0},
    {"id": str(uuid.uuid4()), "name": "八达岭长城", "type": "attraction", "city": "北京", "district": "延庆区",
     "address": "北京市延庆区八达岭镇", "latitude": 40.3597, "longitude": 116.0177,
     "price_range": {"min": 35, "max": 40}, "rating": 4.6, "tags": ["世界遗产", "户外", "长城"],
     "description": "明长城中保存最完好的一段，万里长城的精华所在。", "opening_hours": "06:30-19:00",
     "popularity_score": 94.0},
    {"id": str(uuid.uuid4()), "name": "天坛公园", "type": "attraction", "city": "北京", "district": "东城区",
     "address": "北京市东城区天坛内东里7号", "latitude": 39.8822, "longitude": 116.4066,
     "price_range": {"min": 15, "max": 35}, "rating": 4.6, "tags": ["世界遗产", "历史文化", "公园"],
     "description": "明清两代皇帝祭天的场所，中国古建筑精华。", "opening_hours": "06:00-21:00",
     "popularity_score": 92.0},
    {"id": str(uuid.uuid4()), "name": "鸟巢（国家体育场）", "type": "attraction", "city": "北京", "district": "朝阳区",
     "address": "北京市朝阳区国家体育场南路1号", "latitude": 39.9928, "longitude": 116.3897,
     "price_range": {"min": 50, "max": 100}, "rating": 4.4, "tags": ["现代建筑", "奥运", "打卡"],
     "description": "2008年北京奥运会主体育场，现代建筑地标。", "opening_hours": "09:00-18:00",
     "popularity_score": 88.0},
    # 酒店
    {"id": str(uuid.uuid4()), "name": "北京王府井希尔顿酒店", "type": "hotel", "city": "北京", "district": "东城区",
     "address": "北京市东城区王府井大街8号", "latitude": 39.9150, "longitude": 116.4100,
     "price_range": {"min": 800, "max": 1500}, "rating": 4.7, "tags": ["五星级", "市中心", "商务"],
     "description": "位于王府井商业区，步行可达天安门和故宫。", "popularity_score": 90.0},
    {"id": str(uuid.uuid4()), "name": "北京海淀雅乐轩酒店", "type": "hotel", "city": "北京", "district": "海淀区",
     "address": "北京市海淀区", "latitude": 39.9850, "longitude": 116.3000,
     "price_range": {"min": 400, "max": 700}, "rating": 4.3, "tags": ["四星级", "高校区"],
     "description": "靠近中关村和颐和园，适合商务和旅游出行。", "popularity_score": 75.0},
    # 餐厅
    {"id": str(uuid.uuid4()), "name": "四季民福烤鸭店", "type": "restaurant", "city": "北京", "district": "东城区",
     "address": "北京市东城区南池子大街32号", "latitude": 39.9140, "longitude": 116.4010,
     "price_range": {"min": 150, "max": 300}, "rating": 4.6, "tags": ["烤鸭", "老字号", "必吃"],
     "description": "地道北京烤鸭，皮脆肉嫩，故宫旁边的老店。", "popularity_score": 93.0},
    {"id": str(uuid.uuid4()), "name": "护国寺小吃", "type": "restaurant", "city": "北京", "district": "海淀区",
     "address": "北京市海淀区护国寺街", "latitude": 39.9900, "longitude": 116.2800,
     "price_range": {"min": 30, "max": 80}, "rating": 4.4, "tags": ["小吃", "老字号", "平价"],
     "description": "老北京传统小吃汇聚，豆汁焦圈豌豆黄品种齐全。", "popularity_score": 85.0},

    # ========== 成都 ==========
    {"id": str(uuid.uuid4()), "name": "成都大熊猫繁育研究基地", "type": "attraction", "city": "成都", "district": "成华区",
     "address": "成都市成华区熊猫大道1375号", "latitude": 30.7355, "longitude": 104.1467,
     "price_range": {"min": 55, "max": 55}, "rating": 4.7, "tags": ["亲子", "自然", "国宝"],
     "description": "近距离观察大熊猫的绝佳场所，可以看到不同年龄段的熊猫。", "opening_hours": "07:30-18:00",
     "popularity_score": 96.0},
    {"id": str(uuid.uuid4()), "name": "宽窄巷子", "type": "attraction", "city": "成都", "district": "青羊区",
     "address": "成都市青羊区长顺街", "latitude": 30.6701, "longitude": 104.0524,
     "price_range": {"min": 0, "max": 0}, "rating": 4.5, "tags": ["历史文化", "免费", "美食"],
     "description": "成都保存最完好的清朝古街道，分宽巷子、窄巷子和井巷子。", "opening_hours": "全天",
     "popularity_score": 94.0},
    {"id": str(uuid.uuid4()), "name": "锦里古街", "type": "attraction", "city": "成都", "district": "武侯区",
     "address": "成都市武侯区武侯祠大街231号", "latitude": 30.6455, "longitude": 104.0462,
     "price_range": {"min": 0, "max": 0}, "rating": 4.5, "tags": ["历史文化", "购物", "美食"],
     "description": "西蜀历史上最古老、最具商业气息的街道之一，与武侯祠相邻。", "opening_hours": "全天",
     "popularity_score": 91.0},
    {"id": str(uuid.uuid4()), "name": "武侯祠", "type": "attraction", "city": "成都", "district": "武侯区",
     "address": "成都市武侯区武侯祠大街231号", "latitude": 30.6444, "longitude": 104.0454,
     "price_range": {"min": 50, "max": 50}, "rating": 4.6, "tags": ["历史文化", "三国"],
     "description": "纪念三国时期蜀汉丞相诸葛亮的祠堂，三国文化圣地。", "opening_hours": "08:00-18:00",
     "popularity_score": 90.0},
    {"id": str(uuid.uuid4()), "name": "都江堰景区", "type": "attraction", "city": "成都", "district": "都江堰市",
     "address": "成都市都江堰市公园路", "latitude": 30.9988, "longitude": 103.6130,
     "price_range": {"min": 80, "max": 80}, "rating": 4.6, "tags": ["世界遗产", "水利工程", "自然"],
     "description": "世界文化遗产，两千多年前建造的无坝引水水利工程。", "opening_hours": "08:00-17:30",
     "popularity_score": 89.0},
    {"id": str(uuid.uuid4()), "name": "成都春熙路亚朵酒店", "type": "hotel", "city": "成都", "district": "锦江区",
     "address": "成都市锦江区春熙路", "latitude": 30.6566, "longitude": 104.0818,
     "price_range": {"min": 350, "max": 600}, "rating": 4.5, "tags": ["四星级", "市中心", "设计"],
     "description": "位于春熙路核心商圈，地铁直达，出行便利。", "popularity_score": 82.0},
    {"id": str(uuid.uuid4()), "name": "小龙坎火锅", "type": "restaurant", "city": "成都", "district": "锦江区",
     "address": "成都市锦江区东大街", "latitude": 30.6558, "longitude": 104.0822,
     "price_range": {"min": 80, "max": 200}, "rating": 4.5, "tags": ["火锅", "麻辣", "网红"],
     "description": "成都知名火锅品牌，麻辣鲜香，排队火爆。", "popularity_score": 92.0},

    # ========== 上海 ==========
    {"id": str(uuid.uuid4()), "name": "上海外滩", "type": "attraction", "city": "上海", "district": "黄浦区",
     "address": "上海市黄浦区中山东一路", "latitude": 31.2400, "longitude": 121.4907,
     "price_range": {"min": 0, "max": 0}, "rating": 4.7, "tags": ["地标", "免费", "夜景"],
     "description": "黄浦江畔的万国建筑博览群，上海最具代表性的景观。", "opening_hours": "全天",
     "popularity_score": 97.5},
    {"id": str(uuid.uuid4()), "name": "上海东方明珠广播电视塔", "type": "attraction", "city": "上海", "district": "浦东新区",
     "address": "上海市浦东新区世纪大道1号", "latitude": 31.2397, "longitude": 121.4998,
     "price_range": {"min": 100, "max": 220}, "rating": 4.5, "tags": ["地标", "高空观景", "打卡"],
     "description": "上海地标建筑，可俯瞰浦江两岸全景。", "opening_hours": "08:00-21:30",
     "popularity_score": 95.0},
    {"id": str(uuid.uuid4()), "name": "上海迪士尼乐园", "type": "attraction", "city": "上海", "district": "浦东新区",
     "address": "上海市浦东新区川沙镇", "latitude": 31.1443, "longitude": 121.6594,
     "price_range": {"min": 399, "max": 799}, "rating": 4.6, "tags": ["主题乐园", "亲子", "娱乐"],
     "description": "中国大陆首座迪士尼主题公园，适合全家出游。", "opening_hours": "08:30-20:30",
     "popularity_score": 96.0},
    {"id": str(uuid.uuid4()), "name": "上海豫园", "type": "attraction", "city": "上海", "district": "黄浦区",
     "address": "上海市黄浦区福佑路168号", "latitude": 31.2273, "longitude": 121.4906,
     "price_range": {"min": 30, "max": 40}, "rating": 4.4, "tags": ["园林", "历史文化", "购物"],
     "description": "明朝时期的江南古典园林，与城隍庙相邻。", "opening_hours": "08:30-17:00",
     "popularity_score": 90.0},
    {"id": str(uuid.uuid4()), "name": "上海南京路步行街", "type": "attraction", "city": "上海", "district": "黄浦区",
     "address": "上海市黄浦区南京东路", "latitude": 31.2369, "longitude": 121.4782,
     "price_range": {"min": 0, "max": 0}, "rating": 4.5, "tags": ["购物", "免费", "美食"],
     "description": "中国最著名的商业街之一，中华第一商业街。", "opening_hours": "全天",
     "popularity_score": 93.0},
    {"id": str(uuid.uuid4()), "name": "上海和平饭店", "type": "hotel", "city": "上海", "district": "黄浦区",
     "address": "上海市黄浦区南京东路20号", "latitude": 31.2420, "longitude": 121.4910,
     "price_range": {"min": 1500, "max": 3000}, "rating": 4.8, "tags": ["五星级", "历史建筑", "外滩"],
     "description": "外滩地标性历史酒店，装饰艺术风格典范。", "popularity_score": 88.0},
    {"id": str(uuid.uuid4()), "name": "上海南翔馒头店", "type": "restaurant", "city": "上海", "district": "黄浦区",
     "address": "上海市黄浦区豫园路85号", "latitude": 31.2275, "longitude": 121.4895,
     "price_range": {"min": 50, "max": 150}, "rating": 4.4, "tags": ["小吃", "老字号", "小笼包"],
     "description": "始建于1900年的老字号，以小笼包闻名中外。", "popularity_score": 89.0},
]


def seed_to_mysql():
    """将 POI 数据写入 MySQL poi 表"""
    import asyncio
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
    from sqlalchemy import text

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://smarttravel:smarttravel123@192.168.87.50:3306/smarttravel",
    )

    engine = create_async_engine(DATABASE_URL, echo=True)

    async def _seed():
        async with engine.begin() as conn:
            for poi in POI_DATA:
                await conn.execute(
                    text("""
                        INSERT INTO poi (id, name, type, city, district, address, latitude, longitude,
                                         price_range, rating, tags, description, opening_hours, popularity_score)
                        VALUES (:id, :name, :type, :city, :district, :address, :latitude, :longitude,
                                :price_range, :rating, :tags, :description, :opening_hours, :popularity_score)
                        ON DUPLICATE KEY UPDATE
                            rating=VALUES(rating), popularity_score=VALUES(popularity_score)
                    """),
                    {
                        "id": poi["id"],
                        "name": poi["name"],
                        "type": poi["type"],
                        "city": poi["city"],
                        "district": poi.get("district", ""),
                        "address": poi.get("address", ""),
                        "latitude": poi["latitude"],
                        "longitude": poi["longitude"],
                        "price_range": str(poi.get("price_range", {})),
                        "rating": poi.get("rating", 0),
                        "tags": str(poi.get("tags", [])),
                        "description": poi.get("description", ""),
                        "opening_hours": poi.get("opening_hours", ""),
                        "popularity_score": poi.get("popularity_score", 0),
                    },
                )
            print(f"✅ 成功写入 {len(POI_DATA)} 条 POI 数据到 MySQL")

    asyncio.run(_seed())


def seed_to_es():
    """将 POI 数据批量索引到 Elasticsearch"""
    import asyncio
    from elasticsearch import AsyncElasticsearch

    ES_HOST = os.getenv("ES_HOST", "192.168.87.50")
    ES_PORT = int(os.getenv("ES_PORT", "9200"))

    async def _seed():
        client = AsyncElasticsearch(hosts=[f"http://{ES_HOST}:{ES_PORT}"])

        # 确保索引存在
        from backend.search_service.app.es.mappings import POI_INDEX_MAPPING
        exists = await client.indices.exists(index="poi")
        if not exists:
            await client.indices.create(index="poi", body=POI_INDEX_MAPPING)
            print("✅ 创建 POI 索引")

        # 批量索引
        operations = []
        for poi in POI_DATA:
            doc = {
                "id": poi["id"],
                "name": poi["name"],
                "type": poi["type"],
                "city": poi["city"],
                "district": poi.get("district", ""),
                "address": poi.get("address", ""),
                "location": {"lat": poi["latitude"], "lon": poi["longitude"]},
                "price_range": poi.get("price_range", {}),
                "rating": poi.get("rating", 0),
                "price": poi.get("price_range", {}).get("min", 0),
                "tags": poi.get("tags", []),
                "description": poi.get("description", ""),
                "opening_hours": poi.get("opening_hours", ""),
                "popularity_score": poi.get("popularity_score", 0),
            }
            operations.append({"index": {"_index": "poi", "_id": doc["id"]}})
            operations.append(doc)

        result = await client.bulk(operations=operations, refresh=True)
        if result.get("errors"):
            print(f"⚠️ 部分索引失败，请检查 ES 日志")
        else:
            print(f"✅ 成功将 {len(POI_DATA)} 条 POI 数据索引到 ES")

        await client.close()

    asyncio.run(_seed())


if __name__ == "__main__":
    print("=" * 60)
    print("SmartTravel POI 种子数据初始化")
    print("=" * 60)
    print("\n1. 写入 MySQL...")
    seed_to_mysql()
    print("\n2. 索引到 Elasticsearch...")
    seed_to_es()
    print("\n🎉 POI 种子数据初始化完成！")
