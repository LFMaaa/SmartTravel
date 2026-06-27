import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://smarttravel:smarttravel123@localhost:3306/smarttravel")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Redis 连接（全局单例，懒加载）
_redis_pool: aioredis.Redis | None = None


async def get_redis() -> aioredis.Redis | None:
    """获取 Redis 连接（用于短信验证码缓存等），连接失败返回 None"""
    global _redis_pool
    if _redis_pool is not None:
        return _redis_pool
    try:
        _redis_pool = aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)
        await _redis_pool.ping()
        logger.info(f"Redis 连接成功: {REDIS_URL}")
    except Exception as exc:
        logger.warning(f"Redis 不可用 ({exc})，短信验证码将回退到 MySQL")
        _redis_pool = None
    return _redis_pool


async def get_db() -> AsyncSession:
    """FastAPI 依赖注入：获取数据库会话"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db():
    """启动时创建所有表"""
    from common.models import Base  # noqa: F811
    from .models.user import User, UserPreference  # noqa: F401
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)