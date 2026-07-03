import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "mysql+aiomysql://smarttravel:smarttravel123@localhost:3306/smarttravel")

engine = create_async_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)
async_session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db() -> AsyncSession:
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
    from common.models import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
