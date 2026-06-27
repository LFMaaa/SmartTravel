# -*- coding: utf-8 -*-
"""
ES seed data import script
Usage:
  python scripts/seed_es.py --host localhost --port 9200
"""
import json
import sys
import argparse
import urllib.request
import urllib.error

ES_HOST = "192.168.87.50"
ES_PORT = 9200
POI_INDEX = "poi"


def es_request(method: str, path: str, body: dict = None) -> dict:
    """发送 ES HTTP 请求"""
    url = f"http://{ES_HOST}:{ES_PORT}{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"  ES error {e.code}: {body[:300]}")
        return {"error": body}
    except Exception as e:
        print(f"  Connection error: {e}")
        return {"error": str(e)}


# ============================================================
# 种子数据 — 北京/成都/上海/西安
# ============================================================
SEED_POIS = [
    {"poi_id": "beijing_001", "name": "故宫博物院", "name_suggest": {"input": ["故宫", "故宫博物院", "紫禁城"]}, "type": "attraction", "city": "北京", "district": "东城区", "location": {"lat": 39.9163, "lon": 116.3972}, "price": 60, "rating": 4.8, "tags": ["历史文化", "世界遗产", "博物馆", "亲子"], "description": "世界最大宫殿建筑群，明清两代皇家宫殿", "address": "北京市东城区景山前街4号", "opening_hours": "08:30-17:00", "popularity_score": 98.5},
    {"poi_id": "beijing_002", "name": "天坛公园", "name_suggest": {"input": ["天坛", "天坛公园"]}, "type": "attraction", "city": "北京", "district": "东城区", "location": {"lat": 39.8822, "lon": 116.4066}, "price": 34, "rating": 4.7, "tags": ["历史文化", "世界遗产", "公园"], "description": "明清皇帝祭天场所", "address": "北京市东城区天坛路", "opening_hours": "06:00-21:00", "popularity_score": 92.0},
    {"poi_id": "beijing_003", "name": "颐和园", "name_suggest": {"input": ["颐和园", "皇家园林"]}, "type": "attraction", "city": "北京", "district": "海淀区", "location": {"lat": 39.9999, "lon": 116.2754}, "price": 30, "rating": 4.7, "tags": ["历史文化", "世界遗产", "园林"], "description": "中国现存最大皇家园林", "address": "北京市海淀区新建宫门路19号", "opening_hours": "06:30-18:00", "popularity_score": 91.0},
    {"poi_id": "beijing_004", "name": "八达岭长城", "name_suggest": {"input": ["长城", "八达岭"]}, "type": "attraction", "city": "北京", "district": "延庆区", "location": {"lat": 40.3597, "lon": 116.0200}, "price": 40, "rating": 4.6, "tags": ["世界遗产", "户外", "登山"], "description": "万里长城精华段", "address": "北京市延庆区", "opening_hours": "06:30-19:00", "popularity_score": 89.0},
    {"poi_id": "beijing_005", "name": "南锣鼓巷", "name_suggest": {"input": ["南锣鼓巷", "胡同"]}, "type": "attraction", "city": "北京", "district": "东城区", "location": {"lat": 39.9375, "lon": 116.4034}, "price": 0, "rating": 4.5, "tags": ["胡同", "文艺", "美食"], "description": "北京最古老的街区之一", "address": "北京市东城区南锣鼓巷", "opening_hours": "全天", "popularity_score": 90.0},
    {"poi_id": "beijing_006", "name": "北京王府井希尔顿酒店", "name_suggest": {"input": ["希尔顿", "王府井酒店"]}, "type": "hotel", "city": "北京", "district": "东城区", "location": {"lat": 39.9150, "lon": 116.4100}, "price": 1280, "rating": 4.6, "tags": ["五星级", "市中心"], "description": "位于王府井核心地段，步行可达故宫", "address": "北京市东城区王府井大街", "popularity_score": 88.0},
    {"poi_id": "beijing_007", "name": "四季民福烤鸭店", "name_suggest": {"input": ["烤鸭", "四季民福"]}, "type": "restaurant", "city": "北京", "district": "东城区", "location": {"lat": 39.9140, "lon": 116.4010}, "price": 150, "rating": 4.6, "tags": ["烤鸭", "北京菜", "老字号"], "description": "地道北京烤鸭", "address": "北京市东城区南池子大街", "popularity_score": 93.0},

    {"poi_id": "chengdu_001", "name": "宽窄巷子", "name_suggest": {"input": ["宽窄巷子", "成都"]}, "type": "attraction", "city": "成都", "district": "青羊区", "location": {"lat": 30.6674, "lon": 104.0566}, "price": 0, "rating": 4.5, "tags": ["历史文化", "美食", "街区"], "description": "成都三大历史文化保护区之一", "address": "成都市青羊区长顺街", "opening_hours": "全天", "popularity_score": 95.0},
    {"poi_id": "chengdu_002", "name": "成都大熊猫繁育研究基地", "name_suggest": {"input": ["大熊猫", "熊猫基地"]}, "type": "attraction", "city": "成都", "district": "成华区", "location": {"lat": 30.7351, "lon": 104.1423}, "price": 55, "rating": 4.8, "tags": ["动物", "亲子", "自然"], "description": "近距离观察大熊猫的最佳地点", "address": "成都市成华区熊猫大道1375号", "opening_hours": "07:30-18:00", "popularity_score": 96.0},
    {"poi_id": "chengdu_003", "name": "武侯祠", "name_suggest": {"input": ["武侯祠", "诸葛亮"]}, "type": "attraction", "city": "成都", "district": "武侯区", "location": {"lat": 30.6469, "lon": 104.0448}, "price": 60, "rating": 4.6, "tags": ["历史文化", "三国"], "description": "纪念诸葛亮和刘备的祠庙", "address": "成都市武侯区武侯祠大街231号", "opening_hours": "08:00-18:00", "popularity_score": 88.0},
    {"poi_id": "chengdu_004", "name": "小龙坎老火锅", "name_suggest": {"input": ["小龙坎", "火锅"]}, "type": "restaurant", "city": "成都", "district": "锦江区", "location": {"lat": 30.6558, "lon": 104.0822}, "price": 120, "rating": 4.6, "tags": ["火锅", "川菜"], "description": "成都火锅排队王", "address": "成都市锦江区东大街", "popularity_score": 94.0},

    {"poi_id": "shanghai_001", "name": "外滩", "name_suggest": {"input": ["外滩", "黄浦江"]}, "type": "attraction", "city": "上海", "district": "黄浦区", "location": {"lat": 31.2400, "lon": 121.4904}, "price": 0, "rating": 4.7, "tags": ["城市景观", "夜景", "拍照"], "description": "上海地标", "address": "上海市黄浦区中山东一路", "opening_hours": "全天", "popularity_score": 97.0},
    {"poi_id": "shanghai_002", "name": "上海迪士尼乐园", "name_suggest": {"input": ["迪士尼", "上海迪士尼"]}, "type": "attraction", "city": "上海", "district": "浦东新区", "location": {"lat": 31.1433, "lon": 121.6605}, "price": 499, "rating": 4.6, "tags": ["主题乐园", "亲子", "网红"], "description": "中国大陆首座迪士尼", "address": "上海市浦东新区川沙新镇", "opening_hours": "08:30-20:30", "popularity_score": 94.0},
    {"poi_id": "shanghai_003", "name": "豫园", "name_suggest": {"input": ["豫园", "城隍庙"]}, "type": "attraction", "city": "上海", "district": "黄浦区", "location": {"lat": 31.2272, "lon": 121.4924}, "price": 40, "rating": 4.5, "tags": ["园林", "历史文化", "美食"], "description": "明代江南私家园林", "address": "上海市黄浦区福佑路168号", "opening_hours": "08:30-17:00", "popularity_score": 87.0},

    {"poi_id": "xian_001", "name": "兵马俑", "name_suggest": {"input": ["兵马俑", "秦始皇"]}, "type": "attraction", "city": "西安", "district": "临潼区", "location": {"lat": 34.3852, "lon": 109.2731}, "price": 120, "rating": 4.8, "tags": ["世界遗产", "历史", "博物馆"], "description": "世界第八大奇迹", "address": "西安市临潼区秦陵北路", "opening_hours": "08:30-17:00", "popularity_score": 97.0},
    {"poi_id": "xian_002", "name": "西安城墙", "name_suggest": {"input": ["城墙", "西安城墙"]}, "type": "attraction", "city": "西安", "district": "碑林区", "location": {"lat": 34.2602, "lon": 108.9424}, "price": 54, "rating": 4.6, "tags": ["历史", "古城", "骑行"], "description": "中国现存规模最大的古城墙", "address": "西安市碑林区南大街", "opening_hours": "08:00-22:00", "popularity_score": 92.0},
    {"poi_id": "xian_003", "name": "回民街", "name_suggest": {"input": ["回民街", "小吃"]}, "type": "restaurant", "city": "西安", "district": "莲湖区", "location": {"lat": 34.2635, "lon": 108.9402}, "price": 60, "rating": 4.5, "tags": ["小吃", "美食", "夜市"], "description": "西安最著名的小吃街", "address": "西安市莲湖区回民街", "popularity_score": 93.0},
]


def create_index_simple():
    """用最简配置创建索引（不依赖 ik 分词）"""
    print(">>> 创建 POI 索引（最小化配置）...")
    mapping = {
        "mappings": {
            "properties": {
                "poi_id": {"type": "keyword"},
                "name": {"type": "text"},
                "name_suggest": {"type": "completion"},
                "type": {"type": "keyword"},
                "city": {"type": "keyword"},
                "district": {"type": "keyword"},
                "location": {"type": "geo_point"},
                "price": {"type": "float"},
                "rating": {"type": "float"},
                "tags": {"type": "keyword"},
                "description": {"type": "text"},
                "address": {"type": "text"},
                "opening_hours": {"type": "keyword"},
                "popularity_score": {"type": "float"},
            }
        }
    }

    # 先删除已有索引
    es_request("DELETE", f"/{POI_INDEX}")
    result = es_request("PUT", f"/{POI_INDEX}", mapping)

    if "error" in result:
        print(f"  创建失败: {result['error'][:200]}")
        return False
    print("  索引创建成功")
    return True


def import_pois():
    """逐条导入 POI 数据"""
    print(f">>> 导入 {len(SEED_POIS)} 条 POI 数据...")
    success = 0
    for poi in SEED_POIS:
        doc_id = poi["poi_id"]
        result = es_request("PUT", f"/{POI_INDEX}/_doc/{doc_id}", poi)
        if "error" not in result or result.get("result") == "created" or result.get("result") == "updated":
            success += 1
        else:
            print(f"  失败: {poi['name']} — {result.get('error', '')[:100]}")
    print(f"  成功导入 {success}/{len(SEED_POIS)} 条")
    return success


def verify():
    """验证数据"""
    result = es_request("GET", f"/{POI_INDEX}/_count")
    count = result.get("count", 0)
    print(f">>> 索引 {POI_INDEX} 共 {count} 条文档")

    # 测试搜索
    result = es_request("GET", f"/{POI_INDEX}/_search?q=故宫&size=2")
    hits = result.get("hits", {}).get("hits", [])
    if hits:
        names = [h["_source"]["name"] for h in hits]
        print(f"  搜索'故宫' → {names}")
    else:
        print("  搜索'故宫' → 无结果（可能需要刷新）")

    es_request("POST", f"/{POI_INDEX}/_refresh")
    return count > 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ES POI 种子数据导入")
    parser.add_argument("--host", default="192.168.87.50")
    parser.add_argument("--port", type=int, default=9200)
    args = parser.parse_args()

    ES_HOST = args.host
    ES_PORT = args.port

    print(f"============================================")
    print(f" SmartTravel ES 种子数据导入")
    print(f" ES: http://{ES_HOST}:{ES_PORT}")
    print(f"============================================")

    # 检查连接
    result = es_request("GET", "/")
    if "error" in result:
        print(f"无法连接 ES: {result['error'][:200]}")
        print(f"请确认 ES 容器在运行: docker ps | grep elasticsearch")
        sys.exit(1)
    print(f"ES 版本: {result.get('version', {}).get('number', 'unknown')}")

    if not create_index_simple():
        sys.exit(1)

    import_pois()
    verify()

    print()
    print("快速测试:")
    print(f"  curl 'http://{ES_HOST}:{ES_PORT}/poi/_search?q=故宫&pretty'")
    print(f"  curl 'http://{ES_HOST}:{ES_PORT}/poi/_search?q=city:成都&pretty'")
    print("============================================")
