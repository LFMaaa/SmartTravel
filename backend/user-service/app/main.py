from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import logging

from fastapi import FastAPI

from .api.routes import router as user_router
from .database import init_db, get_redis

load_dotenv()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """启动时：建表 + 预热 Redis"""
    await init_db()
    # 预热 Redis 连接
    redis = await get_redis()
    if redis:
        logger.info("Redis 预热成功")
    else:
        logger.warning("Redis 未连接，短信验证码将使用 MySQL 存储")
    yield


app = FastAPI(
    title="SmartTravel User Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(user_router, prefix="/api/v1/user")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "user-service"}