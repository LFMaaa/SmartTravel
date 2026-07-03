import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import router as itinerary_router
from .database import init_db, is_db_available, async_session_factory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：尝试连接 MySQL 及预检 Dify，不可用时降级"""
    await init_db()
    if is_db_available():
        logger.info("[Startup] MySQL 已连接，使用数据库持久化")
    else:
        logger.warning("[Startup] MySQL 不可用，使用内存模式（数据不持久化）")

    # 预检 LLM 状态，避免首次请求阻塞
    from .services.llm_service import check_llm_health
    await check_llm_health()

    # 启动天气监控后台任务
    from .services.weather_monitor import start_weather_monitor
    await start_weather_monitor(
        db_session_factory=async_session_factory if is_db_available() else None,
        interval_hours=6,
    )
    yield
    # 关闭天气监控
    from .services.weather_monitor import stop_weather_monitor
    await stop_weather_monitor()


app = FastAPI(
    title="SmartTravel Itinerary Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(itinerary_router, prefix="/api/v1/itinerary")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "itinerary-service",
        "database": "connected" if is_db_available() else "memory",
    }
