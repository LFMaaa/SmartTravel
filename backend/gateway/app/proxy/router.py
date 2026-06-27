import httpx
from fastapi import APIRouter, Request
from fastapi.responses import StreamingResponse

proxy_router = APIRouter()

# 服务路由映射
SERVICE_ROUTES = {
    "/user": "http://user-service:8001",
    "/itinerary": "http://itinerary-service:8002",
    "/search": "http://search-service:8003",
    "/payment": "http://payment-service:8004",
    "/notification": "http://notification-service:8005",
}


async def _proxy_request(request: Request, service_url: str, path: str):
    """通用代理转发"""
    async with httpx.AsyncClient(timeout=60.0) as client:
        target_url = f"{service_url}{path}"
        body = await request.body()
        headers = dict(request.headers)
        headers.pop("host", None)

        req = client.build_request(
            method=request.method,
            url=target_url,
            headers=headers,
            content=body,
            params=request.query_params,
        )
        resp = await client.send(req, stream=True)

        return StreamingResponse(
            resp.aiter_bytes(),
            status_code=resp.status_code,
            headers=dict(resp.headers),
        )


@proxy_router.api_route("/user/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_user(request: Request, path: str):
    return await _proxy_request(request, SERVICE_ROUTES["/user"], f"/{path}")


@proxy_router.api_route("/itinerary/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_itinerary(request: Request, path: str):
    return await _proxy_request(request, SERVICE_ROUTES["/itinerary"], f"/{path}")


@proxy_router.api_route("/search/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_search(request: Request, path: str):
    return await _proxy_request(request, SERVICE_ROUTES["/search"], f"/{path}")


@proxy_router.api_route("/payment/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_payment(request: Request, path: str):
    return await _proxy_request(request, SERVICE_ROUTES["/payment"], f"/{path}")


@proxy_router.api_route("/notification/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_notification(request: Request, path: str):
    return await _proxy_request(request, SERVICE_ROUTES["/notification"], f"/{path}")