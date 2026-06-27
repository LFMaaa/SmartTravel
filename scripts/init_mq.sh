#!/bin/bash
# ============================================
# SmartTravel RabbitMQ 初始化脚本
# ============================================

RABBITMQ_HOST="${RABBITMQ_HOST:-localhost}"
RABBITMQ_USER="${RABBITMQ_USER:-smarttravel}"
RABBITMQ_PASS="${RABBITMQ_PASS:-smarttravel123}"
API="http://${RABBITMQ_HOST}:15672/api"

echo "Creating RabbitMQ exchanges and queues..."

# 延迟交换机（需要安装 rabbitmq_delayed_message_exchange 插件）
curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X PUT "${API}/exchanges/%2F/delay.exchange" \
  -H 'Content-Type: application/json' -d '{
    "type": "x-delayed-message",
    "arguments": {"x-delayed-type": "direct"},
    "durable": true
  }'

# 事件交换机
curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X PUT "${API}/exchanges/%2F/event.exchange" \
  -H 'Content-Type: application/json' -d '{
    "type": "topic",
    "durable": true
  }'

# 延迟队列
curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X PUT "${API}/queues/%2F/delay.queue" \
  -H 'Content-Type: application/json' -d '{"durable": true}'

# 行程事件队列
curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X PUT "${API}/queues/%2F/itinerary.event.queue" \
  -H 'Content-Type: application/json' -d '{"durable": true}'

# 通知队列
curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X PUT "${API}/queues/%2F/notification.queue" \
  -H 'Content-Type: application/json' -d '{"durable": true}'

# 绑定关系
curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X POST "${API}/bindings/%2F/e/delay.exchange/q/delay.queue" \
  -H 'Content-Type: application/json' -d '{"routing_key": "payment.timeout"}'

curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X POST "${API}/bindings/%2F/e/event.exchange/q/itinerary.event.queue" \
  -H 'Content-Type: application/json' -d '{"routing_key": "itinerary.event.*"}'

curl -u "${RABBITMQ_USER}:${RABBITMQ_PASS}" -X POST "${API}/bindings/%2F/e/event.exchange/q/notification.queue" \
  -H 'Content-Type: application/json' -d '{"routing_key": "notification.#"}'

echo ""
echo "RabbitMQ exchanges and queues created successfully!"