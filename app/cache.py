# app/cache.py
import os
import json
from redis import Redis

# If you run Redis in Docker, use `localhost`
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)

def cache_set(key: str, value: dict, ex: int = 300):
    redis_client.set(key, json.dumps(value), ex=ex)

def cache_get(key: str):
    raw = redis_client.get(key)
    if not raw:
        return None
    try:
        return json.loads(raw)
    except Exception:
        return None

def cache_delete(key: str):
    redis_client.delete(key)
        