import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+aiomysql://smarttravel:smarttravel123@192.168.87.50:3306/smarttravel",
)

_db_available = False

try:
    engine = create_async_engine(DATABASE_URL, echo=False, pool_size=10, max_overflow=20)
    async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
except Exception as e:
    logger.warning(f"MySQL 连接配置失败: {e}，将使用无数据库模式")
    engine = None
    async_session_factory = None


async def get_db() -> AsyncSession:
    """FastAPI 依赖注入：获取数据库会话"""
    if async_session_factory is None:
        raise RuntimeError("MySQL 不可用")
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
    """启动时创建所有表。MySQL 不可用时跳过。"""
    global _db_available
    if engine is None:
        logger.warning("[DB] MySQL 不可用，跳过数据库初始化（无数据库模式）")
        _db_available = False
        return

    try:
        from common.models import Base
        from .models.itinerary import Itinerary, ItineraryDay, DayActivity, ItineraryVersion  # noqa: F401
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        _db_available = True
        logger.info("[DB] MySQL 连接成功，数据库表已就绪")
    except Exception as e:
        logger.warning(f"[DB] MySQL 连接失败: {e}，将使用无数据库模式")
        _db_available = False


def is_db_available() -> bool:
    return _db_available
