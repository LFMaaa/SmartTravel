"""
天气监控 + 短信提醒调度器

流程:
  1. 每天定时检查所有活跃行程 (status=planned/in_progress)
  2. 调用天气 API 获取目的地未来天气预报
  3. 如果天气不适合行程（暴雨/台风/高温/寒潮等）:
     → 发送 MQ 事件到 notification-service
     → notification-service 通过 WebSocket + SMS 推送提醒
     → 用户收到提醒后可触发动态重排

天气 API: 后续接入高德天气 API
  当前阶段: 用模拟数据演示完整流程，后续替换为真实 API 调用

配置:
  WEATHER_API_KEY  — 高德/和风天气 API Key (后续)
  AMAP_API_KEY     — 高德地图 API Key (后续)
"""
import asyncio
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# 恶劣天气关键词
BAD_WEATHER_KEYWORDS = [
    "暴雨", "台风", "大雪", "暴雪", "高温", "寒潮", "大风", "冰雹",
    "雷电", "雾霾", "沙尘暴", "大雾",
]


class WeatherMonitor:
    """天气监控调度器"""

    @staticmethod
    async def check_and_alert(db=None, mq_client=None):
        """检查所有活跃行程的天气，必要时发送提醒

        后续集成真实天气 API 后替换 _mock_weather_check
        """
        logger.info("[WeatherMonitor] 开始天气检查...")

        if db is None:
            logger.warning("[WeatherMonitor] DB 不可用，跳过天气检查")
            return

        try:
            from sqlalchemy import select
            from ..models.itinerary import Itinerary

            # 查询所有活跃行程
            result = await db.execute(
                select(Itinerary).where(
                    Itinerary.status.in_(["planned", "in_progress"])
                )
            )
            itineraries = result.scalars().all()

            for it in itineraries:
                # 检查目的地天气
                weather = await WeatherMonitor._get_weather(it.destination)
                bad_conditions = WeatherMonitor._check_bad_weather(weather)

                if bad_conditions:
                    logger.warning(
                        f"[WeatherMonitor] ⚠️ {it.destination} 未来天气不适合行程 {it.id}: "
                        f"{bad_conditions}"
                    )
                    # 发送提醒
                    await WeatherMonitor._send_alert(
                        db=db,
                        mq_client=mq_client,
                        user_id=it.user_id,
                        itinerary_id=it.id,
                        destination=it.destination,
                        bad_conditions=bad_conditions,
                        weather=weather,
                    )
                else:
                    logger.info(f"[WeatherMonitor] ✓ {it.destination} 天气正常")

            logger.info(f"[WeatherMonitor] 检查完成，共 {len(itineraries)} 个活跃行程")

        except Exception as e:
            logger.error(f"[WeatherMonitor] 检查失败: {e}")

    @staticmethod
    async def _get_weather(city: str) -> dict:
        """获取城市未来天气 — 高德天气 API

        GET https://restapi.amap.com/v3/weather/weatherInfo?city={city}&key={key}&extensions=all

        返回格式:
        {
          "city": "北京",
          "forecast": [
            {"date": "2026-06-30", "day_weather": "雷阵雨", "night_weather": "雷阵雨",
             "high_temp": "27", "low_temp": "20", "wind": "东风1-3级"},
            ...
          ],
          "source": "amap"
        }
        """
        import os
        import httpx

        api_key = os.getenv("AMAP_API_KEY", "").strip()
        if not api_key:
            logger.warning("[WeatherMonitor] AMAP_API_KEY 未配置，使用模拟数据")
            return WeatherMonitor._mock_weather(city)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # 高德天气 API: city 参数支持城市名或 adcode
                resp = await client.get(
                    "https://restapi.amap.com/v3/weather/weatherInfo",
                    params={
                        "city": city,
                        "key": api_key,
                        "extensions": "all",  # all=多日预报, base=实时天气
                    },
                )
                resp.raise_for_status()
                data = resp.json()

                if data.get("status") != "1" or data.get("infocode") != "10000":
                    logger.warning(
                        f"[WeatherMonitor] 高德天气 API 返回异常: "
                        f"status={data.get('status')}, info={data.get('info')}"
                    )
                    return WeatherMonitor._mock_weather(city)

                # 解析高德返回格式
                forecasts = data.get("forecasts", [])
                if not forecasts:
                    logger.warning(f"[WeatherMonitor] {city} 无天气数据")
                    return WeatherMonitor._mock_weather(city)

                casts = forecasts[0].get("casts", [])
                result = {
                    "city": forecasts[0].get("city", city),
                    "forecast": [
                        {
                            "date": c.get("date", ""),
                            "day_weather": c.get("dayweather", ""),
                            "night_weather": c.get("nightweather", ""),
                            "high_temp": c.get("daytemp", ""),
                            "low_temp": c.get("nighttemp", ""),
                            "wind": f"{c.get('daywind', '')}风{c.get('daypower', '')}级",
                        }
                        for c in casts
                    ],
                    "source": "amap",
                }

                logger.info(f"[WeatherMonitor] {city} 天气获取成功: {len(casts)}天预报")
                return result

        except Exception as e:
            logger.error(f"[WeatherMonitor] 高德天气 API 调用失败: {e}")
            return WeatherMonitor._mock_weather(city)

    @staticmethod
    def _mock_weather(city: str) -> dict:
        """天气 API 不可用时的模拟数据"""
        return {
            "city": city,
            "forecast": [
                {"date": (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d"),
                 "day_weather": "晴", "night_weather": "多云",
                 "high_temp": "32", "low_temp": "24", "wind": "微风"}
                for i in range(3)
            ],
            "source": "mock",
        }

    @staticmethod
    def _check_bad_weather(weather: dict) -> list[str]:
        """检查天气是否包含恶劣条件"""
        bad = []
        for forecast in weather.get("forecast", []):
            for keyword in BAD_WEATHER_KEYWORDS:
                day = forecast.get("day_weather", "")
                night = forecast.get("night_weather", "")
                if keyword in day or keyword in night:
                    bad.append(f"{forecast['date']}: {keyword}")
        return bad

    @staticmethod
    async def _send_alert(
        db, mq_client, user_id: str, itinerary_id: str,
        destination: str, bad_conditions: list[str], weather: dict,
    ):
        """发送天气提醒：MQ 事件 → notification-service → WebSocket + SMS"""

        # 1. 保存到通知表
        from ..models.itinerary import Itinerary
        from sqlalchemy import select

        try:
            # 标记行程天气预警
            result = await db.execute(select(Itinerary).where(Itinerary.id == itinerary_id))
            itinerary = result.scalar_one_or_none()
            if itinerary and itinerary.day_notes:
                # 更新行程备注
                pass
        except Exception:
            pass

        # 2. 通过 MQ 发送通知事件
        if mq_client:
            try:
                import json
                notification = {
                    "type": "weather_alert",
                    "user_id": user_id,
                    "itinerary_id": itinerary_id,
                    "title": f"⛈️ {destination} 天气预警",
                    "content": {
                        "destination": destination,
                        "bad_conditions": bad_conditions,
                        "forecast": weather.get("forecast", []),
                        "message": f"{destination} 未来天气: {', '.join(bad_conditions)}，建议调整行程安排",
                        "action": "replan",
                    },
                    "resource_type": "itinerary",
                    "resource_id": itinerary_id,
                }
                # 发布到 RabbitMQ
                mq_client.publish(
                    exchange="smarttravel.events",
                    routing_key="weather.alert",
                    message=json.dumps(notification, ensure_ascii=False),
                )
                logger.info(f"[WeatherMonitor] 已发送 MQ 事件: weather.alert → user={user_id}")
            except Exception as e:
                logger.error(f"[WeatherMonitor] MQ 发布失败: {e}")

        # 3. 通过 HTTP 直接调用 notification-service（MQ 不可用时的兜底）
        try:
            import httpx
            async with httpx.AsyncClient(timeout=5.0) as client:
                await client.post(
                    "http://notification-service:8005/api/v1/notification/push",
                    json={
                        "user_id": user_id,
                        "type": "weather_alert",
                        "title": f"⛈️ {destination} 天气预警",
                        "content": {
                            "destination": destination,
                            "bad_conditions": bad_conditions,
                            "message": f"{destination} 未来天气: {', '.join(bad_conditions)}，建议调整行程",
                        },
                        "resource_type": "itinerary",
                        "resource_id": itinerary_id,
                    },
                )
                logger.info(f"[WeatherMonitor] HTTP 通知已发送: user={user_id}")
        except Exception:
            pass

        logger.info(
            f"[WeatherMonitor] 天气预警已发送: user={user_id}, "
            f"destination={destination}, conditions={bad_conditions}"
        )


# ============================================================
# 定时调度器
# ============================================================
_weather_task: asyncio.Task | None = None


async def start_weather_monitor(
    db_session_factory=None,
    mq_client=None,
    interval_hours: int = 6,
):
    """启动天气监控后台任务

    每 interval_hours 小时检查一次所有活跃行程的天气
    """
    global _weather_task

    async def _loop():
        logger.info(f"[WeatherMonitor] 后台任务已启动，检查间隔: {interval_hours}h")
        while True:
            try:
                if db_session_factory:
                    async with db_session_factory() as db:
                        await WeatherMonitor.check_and_alert(db=db, mq_client=mq_client)
                        await db.commit()
                else:
                    logger.warning("[WeatherMonitor] DB 不可用，跳过本轮检查")
            except Exception as e:
                logger.error(f"[WeatherMonitor] 后台任务异常: {e}")

            await asyncio.sleep(interval_hours * 3600)

    _weather_task = asyncio.create_task(_loop())
    return _weather_task


async def stop_weather_monitor():
    """停止天气监控"""
    global _weather_task
    if _weather_task:
        _weather_task.cancel()
        _weather_task = None
        logger.info("[WeatherMonitor] 后台任务已停止")
