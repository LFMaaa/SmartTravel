#!/bin/bash
# ============================================================
# fix_env_files.sh
# 修复智慧旅游项目各微服务缺失的 .env 文件
# 使用方法：在服务器项目根目录（智慧旅游/）下执行
#   bash fix_env_files.sh
# ============================================================

set -e
echo "========================================="
echo "  智游 SmartTravel - 修复 .env 文件"
echo "========================================="

# ---------- gateway ----------
cat > backend/gateway/.env << 'EOF'
JWT_SECRET_KEY=smarttravel-prod-secret-key
EOF
echo "[OK] gateway/.env 已创建"

# ---------- itinerary-service ----------
cat > backend/itinerary-service/.env << 'EOF'
DATABASE_URL=mysql+aiomysql://smarttravel:smarttravel123@127.0.0.1:3306/smarttravel
REDIS_URL=redis://127.0.0.1:6379/0
DIFY_BASE_URL=http://127.0.0.1:80
DIFY_API_KEY=your_dify_api_key_here
JWT_SECRET_KEY=smarttravel-prod-secret-key
EOF
echo "[OK] itinerary-service/.env 已创建"

# ---------- search-service ----------
cat > backend/search-service/.env << 'EOF'
ES_HOST=127.0.0.1
ES_PORT=9200
EOF
echo "[OK] search-service/.env 已创建"

# ---------- payment-service ----------
cat > backend/payment-service/.env << 'EOF'
DATABASE_URL=mysql+aiomysql://smarttravel:smarttravel123@127.0.0.1:3306/smarttravel
REDIS_URL=redis://127.0.0.1:6379/0
RABBITMQ_URL=amqp://smarttravel:smarttravel123@127.0.0.1:5672/
JWT_SECRET_KEY=smarttravel-prod-secret-key
EOF
echo "[OK] payment-service/.env 已创建"

# ---------- notification-service ----------
cat > backend/notification-service/.env << 'EOF'
DATABASE_URL=mysql+aiomysql://smarttravel:smarttravel123@127.0.0.1:3306/smarttravel
RABBITMQ_URL=amqp://smarttravel:smarttravel123@127.0.0.1:5672/
JWT_SECRET_KEY=smarttravel-prod-secret-key
EOF
echo "[OK] notification-service/.env 已创建"

# ---------- 验证 ----------
echo ""
echo "========== 验证结果 =========="
for svc in gateway user-service itinerary-service search-service payment-service notification-service; do
    if [ -f "backend/$svc/.env" ]; then
        echo "✓ backend/$svc/.env"
    else
        echo "✗ backend/$svc/.env  [缺失!]"
    fi
done

echo ""
echo "全部完成！如需查看内容，执行："
echo "  for svc in gateway user-service itinerary-service search-service payment-service notification-service; do echo \"=== \$svc ===\"; cat backend/\$svc/.env; done"
