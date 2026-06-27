from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from .api.routes import router as search_router
from .services.es_service import ESService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时确保 ES 索引存在"""
    try:
        await ESService.ensure_index()
    except Exception:
        import logging
        logging.warning("Elasticsearch 不可用，搜索服务将降级运行")
    yield


app = FastAPI(
    title="SmartTravel Search Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(search_router, prefix="/api/v1/search")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "search-service"}
