"""完整端到端测试 - 模拟API路由的Dify调用"""
import asyncio
import os
import sys

from dotenv import load_dotenv
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "itinerary-service", ".env")
load_dotenv(env_path)
print(f"DIFY_BASE_URL={os.getenv('DIFY_BASE_URL')}")

sys.path.insert(0, "D:/Python_note/my_code/Project/智慧旅游/backend/itinerary-service")
sys.path.insert(0, "D:/Python_note/my_code/Project/智慧旅游/backend")

import logging
logging.basicConfig(level=logging.INFO)

# 模拟数据库 session
from unittest.mock import AsyncMock, MagicMock

from app.services.ai_service import AIService
from app.dify.client import check_dify_health, is_dify_available

async def test():
    # 检查Dify状态
    dify_ok = await check_dify_health()
    print(f"\nDify available: {dify_ok}")

    if not dify_ok:
        print("SKIP: Dify not available")
        return

    # 创建 mock db
    mock_db = AsyncMock()
    mock_db.add = MagicMock()
    mock_db.commit = AsyncMock()
    mock_db.refresh = AsyncMock()
    
    # 模拟 create_itinerary 返回
    from unittest.mock import patch
    from app.services import itinerary_crud_service
    
    fake_result = {"id": "test-id", "title": "test", "days": []}
    itinerary_crud_service.ItineraryCRUDService.create_itinerary = AsyncMock(return_value=fake_result)
    
    print("Calling AIService.generate()...")
    result = await AIService.generate(mock_db, "test_user", "三天杭州浪漫之旅")
    
    print(f"\nResult title: {result.get('title')}")
    print(f"Result destination: {result.get('destination')}")
    print(f"Result days: {len(result.get('days', []))}")
    
    for d in result.get('days', [])[:2]:
        print(f"  Day {d.get('day_index')}:")
        for a in d.get('activities', []):
            print(f"    - {a.get('name')} ({a.get('type')}) @ {a.get('address')} ¥{a.get('price')}")
        if d.get('hotel'):
            print(f"    Hotel: {d['hotel'].get('name')} ¥{d['hotel'].get('price')}")

    # 判断是否是 mock 数据
    is_mock = "推荐景点" in str(result) or "特色餐厅" in str(result)
    print(f"\n{'!!! STILL USING MOCK !!!' if is_mock else 'SUCCESS: DIFY DATA'}")

asyncio.run(test())
