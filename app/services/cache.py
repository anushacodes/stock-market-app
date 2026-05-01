import os
import json
import redis
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

def get_cached_price(ticker: str):
    try:
        data = redis_client.get(f"price:{ticker.upper()}")
        if data:
            return json.loads(data)
    except Exception:
        pass
    return None

def set_cached_price(ticker: str, data: dict, ttl: int = 300):
    try:
        redis_client.setex(f"price:{ticker.upper()}", ttl, json.dumps(data))
    except Exception:
        pass