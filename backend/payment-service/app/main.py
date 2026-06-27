from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI

from .api.routes import router as payment_router
from .api.member_routes import router as member_router
from .api.booking_routes import router as booking_router
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时创建数据库表"""
    await init_db()
    yield


app = FastAPI(
    title="SmartTravel Payment Service",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(payment_router, prefix="/api/v1/payment")
app.include_router(member_router, prefix="/api/v1/payment")
app.include_router(booking_router, prefix="/api/v1/payment")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "payment-service"}
