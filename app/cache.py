import os
import json
from redis import Redis, RedisError

# Redis URL, defaults to localhost if not set
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Initialize Redis client safely
redis_client = None
try:
    redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
except Exception as e:
    print(f"Warning: Redis client could not be initialized: {e}")

def cache_set(key: str, value: dict, ex: int = 300):
    """Safely set a key in Redis. Does nothing if Redis is unavailable."""
    if redis_client is None:
        return
    try:
        redis_client.set(key, json.dumps(value), ex=ex)
    except RedisError as e:
        print(f"Cache set warning: {e}")
    except Exception as e:
        print(f"Cache set unexpected error: {e}")

def cache_get(key: str):
    """Safely get a key from Redis. Returns None if unavailable or invalid."""
    if redis_client is None:
        return None
    try:
        raw = redis_client.get(key)
        if not raw:
            return None
        return json.loads(raw)
    except RedisError as e:
        print(f"Cache get warning: {e}")
        return None
    except Exception as e:
        print(f"Cache get unexpected error: {e}")
        return None

def cache_delete(key: str):
    """Safely delete a key from Redis. Does nothing if Redis is unavailable."""
    if redis_client is None:
        return
    try:
        redis_client.delete(key)
    except RedisError as e:
        print(f"Cache delete warning: {e}")
    except Exception as e:
        print(f"Cache delete unexpected error: {e}")
