from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware.auth import JWTAuthMiddleware
from .proxy.router import proxy_router

app = FastAPI(title="SmartTravel API Gateway", version="0.1.0")

# CORS（开发 + Docker 部署兼容）
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite 开发服务器
        "http://localhost:80",     # Docker Nginx 入口
        "http://localhost",        # Docker Nginx（无端口）
        "http://127.0.0.1",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT 鉴权中间件
app.add_middleware(JWTAuthMiddleware)

# 服务路由转发
app.include_router(proxy_router, prefix="/api/v1")


@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "gateway"}