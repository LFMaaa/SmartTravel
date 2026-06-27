"""直接测试 AIService._generate_via_dify"""
import asyncio
import os
import sys

# MUST load .env and set env vars BEFORE any project imports
from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "itinerary-service", ".env")
load_dotenv(env_path)
print(f"Loaded .env from: {env_path}")
print(f"DIFY_BASE_URL = {os.getenv('DIFY_BASE_URL')}")

# Now safe to import project modules
sys.path.insert(0, "D:/Python_note/my_code/Project/智慧旅游/backend/itinerary-service")
sys.path.insert(0, "D:/Python_note/my_code/Project/智慧旅游/backend")

import logging
import traceback
logging.basicConfig(level=logging.INFO)

from app.dify.client import DIFY_BASE_URL as CURRENT_DIFY_URL
print(f"Client DIFY_BASE_URL = {CURRENT_DIFY_URL}")

from app.services.ai_service import AIService

async def test():
    print("Testing Dify generation directly...")
    try:
        result = await AIService._generate_via_dify(None, "test_user", "三天杭州浪漫之旅")
        print(f"SUCCESS: {result.get('title')}, {len(result.get('days',[]))} days")
        for d in result.get('days', [])[:1]:
            print(f"  Day {d.get('day_index')}:")
            for a in d.get('activities', []):
                print(f"    - {a.get('name')} @ {a.get('address')} (¥{a.get('price')})")
            if d.get('hotel'):
                print(f"    Hotel: {d['hotel'].get('name')} (¥{d['hotel'].get('price')})")
    except Exception as e:
        print(f"FAILED: {e}")
        traceback.print_exc()

asyncio.run(test())
