#!/bin/bash
# ============================================
# SmartTravel ES 一键初始化
# ============================================
set -e

ES_HOST="${ES_HOST:-192.168.87.50:9200}"
echo "============================================"
echo " SmartTravel ES 初始化"
echo " ES Host: http://${ES_HOST}"
echo "============================================"

# 检查连接
echo ""
echo ">>> 检查 ES 连接..."
if ! curl -s --connect-timeout 5 --max-time 10 "http://${ES_HOST}/" > /dev/null 2>&1; then
    echo "  错误: 无法连接 ES (http://${ES_HOST})"
    echo "  请确认: docker ps | grep elasticsearch"
    exit 1
fi
echo "  ES 连接正常"

# 用 Python 脚本完成索引创建 + 数据导入
echo ""
python3 scripts/seed_es.py --host "$(echo $ES_HOST | cut -d: -f1)" --port "$(echo $ES_HOST | cut -d: -f2)"

echo ""
echo "============================================"
