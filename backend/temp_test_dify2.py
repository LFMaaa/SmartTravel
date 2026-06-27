"""测试意图解析输出格式 + 行程生成工作流"""
import asyncio
import json
import httpx

DIFY_BASE_URL = "http://localhost:80"
INTENT_KEY = "app-2XOCKXdJkSyBsLeR7o8JTG30"
GENERATOR_KEY = "app-2ccAvTt3JVl7UmMATtDF9Dbe"

async def test():
    async with httpx.AsyncClient(
        base_url=DIFY_BASE_URL,
        timeout=httpx.Timeout(120.0, connect=5.0),
    ) as c:
        # Test 1: Intent parser - see output format
        print("=== Test 1: 意图解析 ===")
        r1 = await c.post("/v1/workflows/run", json={
            "inputs": {"user_query": "三天杭州浪漫之旅 预算5000"},
            "response_mode": "blocking",
            "user": "test",
        }, headers={"Authorization": f"Bearer {INTENT_KEY}", "Content-Type": "application/json"})
        d1 = r1.json()
        print(f"Status: {r1.status_code}")
        outputs = d1.get("data", {}).get("outputs", {})
        print(f"Outputs: {json.dumps(outputs, ensure_ascii=False, indent=2)}")
        
        # Parse parsed_intent
        raw = outputs.get("parsed_intent", "")
        print(f"\n原始 parsed_intent: {raw}")
        
        # Parse semicolon-separated
        parsed = {}
        for part in raw.split(";"):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                parsed[k.strip()] = v.strip()
        print(f"解析结果: {json.dumps(parsed, ensure_ascii=False, indent=2)}")
        
        # Test 2: Generator workflow - pass parsed_intent directly
        print("\n=== Test 2: 行程生成 ===")
        parsed_intent_str = raw
        print(f"Input parsed_intent: {parsed_intent_str[:100]}")
        r2 = await c.post("/v1/workflows/run", json={
            "inputs": {"parsed_intent": parsed_intent_str},
            "response_mode": "blocking",
            "user": "test",
        }, headers={"Authorization": f"Bearer {GENERATOR_KEY}", "Content-Type": "application/json"})
        print(f"Status: {r2.status_code}")
        if r2.status_code == 200:
            d2 = r2.json()
            outputs2 = d2.get("data", {}).get("outputs", {})
            print(f"Outputs keys: {list(outputs2.keys())}")
            for k, v in outputs2.items():
                v_str = json.dumps(v, ensure_ascii=False)
                print(f"  {k}: {v_str[:500]}")
        else:
            print(f"Error: {r2.text[:300]}")

asyncio.run(test())
