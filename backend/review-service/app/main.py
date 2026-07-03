from contextlib import asynccontextmanager
from dotenv import load_dotenv
import logging

load_dotenv()

from fastapi import FastAPI

from .api.routes import router as review_router
from .database import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    logger.info("[ReviewService] 数据库已就绪")
    yield


app = FastAPI(title="SmartTravel Review Service", version="0.1.0", lifespan=lifespan)
app.include_router(review_router, prefix="/api/v1/review")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "review-service"}
