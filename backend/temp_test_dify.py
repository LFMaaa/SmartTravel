"""直接测试 Dify API 调用"""
import asyncio
import json
import httpx

DIFY_BASE_URL = "http://localhost:80"
INTENT_KEY = "app-2XOCKXdJkSyBsLeR7o8JTG30"

async def test_dify():
    async with httpx.AsyncClient(
        base_url=DIFY_BASE_URL,
        timeout=httpx.Timeout(30.0, connect=5.0),
        headers={
            "Authorization": f"Bearer {INTENT_KEY}",
            "Content-Type": "application/json",
        },
    ) as c:
        # Test 1: GET health check
        print("=== Test 1: GET /v1/workflows/run ===")
        r = await c.get("/v1/workflows/run")
        print(f"  Status: {r.status_code}")
        print(f"  Body: {r.text[:200]}")
        
        # Test 2: POST actual workflow
        print("\n=== Test 2: POST /v1/workflows/run ===")
        payload = {
            "inputs": {"user_query": "三天北京旅行"},
            "response_mode": "blocking",
            "user": "test-user",
        }
        r = await c.post("/v1/workflows/run", json=payload)
        print(f"  Status: {r.status_code}")
        body = r.text[:500]
        print(f"  Body: {body}")
        
        # Test 3: List workflows / apps
        print("\n=== Test 3: GET /v1/apps ===")
        try:
            r = await c.get("/v1/apps")
            print(f"  Status: {r.status_code}")
            print(f"  Body: {r.text[:300]}")
        except Exception as e:
            print(f"  Error: {e}")
        
        # Test 4: Check /console/api
        print("\n=== Test 4: GET /console/api/apps ===")
        try:
            r = await c.get("/console/api/apps")
            print(f"  Status: {r.status_code}")
            print(f"  Body: {r.text[:300]}")
        except Exception as e:
            print(f"  Error: {e}")

asyncio.run(test_dify())
