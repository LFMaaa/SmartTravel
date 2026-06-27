# ES 索引 Mapping 定义
# 参考智旅执行流程文档 §Step 2.3

POI_INDEX_MAPPING = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "analysis": {
            "analyzer": {
                "ik_max_word_analyzer": {
                    "type": "custom",
                    "tokenizer": "ik_max_word"
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "poi_id":           {"type": "keyword"},
            "name":             {"type": "text", "analyzer": "ik_max_word_analyzer"},
            "name_suggest":     {"type": "completion"},
            "type":             {"type": "keyword"},
            "city":             {"type": "keyword"},
            "district":         {"type": "keyword"},
            "location":         {"type": "geo_point"},
            "price_range":      {"type": "integer_range"},
            "price":            {"type": "float"},
            "rating":           {"type": "float"},
            "tags":             {"type": "keyword"},
            "description":      {"type": "text", "analyzer": "ik_max_word_analyzer"},
            "address":          {"type": "text"},
            "opening_hours":    {"type": "keyword"},
            "image_url":        {"type": "keyword", "index": False},
            "popularity_score": {"type": "float"},
            "created_at":       {"type": "date"},
            "updated_at":       {"type": "date"},
        }
    },
}
