from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# 不需要鉴权的路径（Gateway 层放行，鉴权由各微服务自行处理）
PUBLIC_PATHS = {
    "/api/v1/user/login",
    "/api/v1/user/register",
    "/api/v1/user/sms/",
    "/api/v1/user/wechat/",
    "/api/v1/user/oauth/",
    "/api/v1/user/refresh",
    "/api/v1/search/",       # 搜索公开
    "/api/v1/itinerary/",    # 行程服务自行鉴权
    "/health",
    "/docs",
    "/openapi.json",
}


class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 公开路径跳过鉴权
        path = request.url.path
        if any(path.startswith(p) for p in PUBLIC_PATHS):
            return await call_next(request)

        # 从请求头提取 token
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={"code": 401, "message": "未提供认证令牌"},
            )

        token = auth_header.replace("Bearer ", "")
        # 将 token 透传给下游微服务（Starlette Headers 不可变，通过 scope 写入）
        request.scope["headers"] = list(request.scope["headers"]) + [
            (b"x-user-token", token.encode())
        ]
        return await call_next(request)