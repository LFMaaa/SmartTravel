"""
SmartTravel RabbitMQ 消息队列公共模块
使用 aio-pika 实现异步消息发布/消费
"""
import os
import json
import logging
from typing import Callable, Awaitable

import aio_pika
from aio_pika import Message, DeliveryMode, ExchangeType
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel

logger = logging.getLogger("smarttravel.mq")

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://smarttravel:smarttravel123@192.168.87.50:5672/")

# 交换机常量
EXCHANGE_SMARTTRAVEL = "smarttravel.events"
EXCHANGE_DELAYED = "smarttravel.delayed"

# 队列常量
QUEUE_NOTIFICATION = "smarttravel.notification"
QUEUE_PAYMENT_TIMEOUT = "smarttravel.payment.timeout"
QUEUE_REPLAN = "smarttravel.replan"

# 路由键
RK_ORDER_CREATED = "smarttravel.order.created"
RK_ORDER_PAID = "smarttravel.order.paid"
RK_ORDER_TIMEOUT = "smarttravel.order.timeout"
RK_REPLAN_GENERATED = "smarttravel.replan.generated"
RK_WEATHER_ALERT = "smarttravel.weather.alert"


class MQClient:
    """RabbitMQ 客户端（单连接复用）"""

    _connection: AbstractRobustConnection | None = None
    _channel: AbstractRobustChannel | None = None

    @classmethod
    async def get_channel(cls) -> AbstractRobustChannel:
        """懒加载获取信道"""
        if cls._channel is None or cls._channel.is_closed:
            try:
                cls._connection = await aio_pika.connect_robust(RABBITMQ_URL)
                cls._channel = await cls._connection.channel()

                # 声明主题交换机
                await cls._channel.declare_exchange(
                    EXCHANGE_SMARTTRAVEL,
                    ExchangeType.TOPIC,
                    durable=True,
                )

                # 声明延迟交换机（需安装 rabbitmq_delayed_message_exchange 插件）
                try:
                    await cls._channel.declare_exchange(
                        EXCHANGE_DELAYED,
                        ExchangeType.HEADERS,
                        durable=True,
                        arguments={"x-delayed-type": "topic"},
                    )
                except Exception:
                    logger.warning("延迟交换机创建失败，请确保已安装 rabbitmq_delayed_message_exchange 插件")

                logger.info("RabbitMQ 连接成功")
            except Exception as e:
                logger.warning(f"RabbitMQ 连接失败: {e}")
                raise
        return cls._channel

    @classmethod
    async def publish(cls, routing_key: str, message: dict, delayed_seconds: int = 0):
        """发布消息"""
        try:
            channel = await cls.get_channel()
            exchange_name = EXCHANGE_DELAYED if delayed_seconds > 0 else EXCHANGE_SMARTTRAVEL

            # 获取交换机
            exchange = await channel.get_exchange(exchange_name, ensure=True)

            msg = Message(
                body=json.dumps(message, ensure_ascii=False).encode(),
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json",
            )

            # 延迟消息
            if delayed_seconds > 0:
                msg.headers = {"x-delay": delayed_seconds * 1000}

            await exchange.publish(msg, routing_key=routing_key)
        except Exception as e:
            logger.warning(f"MQ 发布失败 [{routing_key}]: {e}")

    @classmethod
    async def start_consumer(
        cls,
        queue_name: str,
        routing_keys: list[str],
        callback: Callable[[dict], Awaitable[None]],
        exchange_name: str = EXCHANGE_SMARTTRAVEL,
    ):
        """启动消息消费者"""
        try:
            channel = await cls.get_channel()
            exchange = await channel.get_exchange(exchange_name, ensure=True)

            # 声明队列
            queue = await channel.declare_queue(queue_name, durable=True)

            # 绑定路由键
            for rk in routing_keys:
                await queue.bind(exchange, routing_key=rk)

            # 开始消费
            async def on_message(message: aio_pika.IncomingMessage):
                async with message.process():
                    try:
                        data = json.loads(message.body.decode())
                        await callback(data)
                    except Exception as e:
                        logger.error(f"MQ 消息处理失败 [{queue_name}]: {e}")

            await queue.consume(on_message)
            logger.info(f"开始消费队列: {queue_name}, 路由键: {routing_keys}")
        except Exception as e:
            logger.warning(f"MQ 消费者启动失败 [{queue_name}]: {e}")

    @classmethod
    async def close(cls):
        """关闭连接"""
        if cls._channel and not cls._channel.is_closed:
            await cls._channel.close()
        if cls._connection and not cls._connection.is_closed:
            await cls._connection.close()
        cls._channel = None
        cls._connection = None
