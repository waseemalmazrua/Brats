import json
from app.core.redis_client import r

def get_cache_key(data: dict) -> str:
    return json.dumps(data, sort_keys=True)


def get_cached_prediction(data: dict):
    key = get_cache_key(data)
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return None


def set_cached_prediction(data: dict, result: dict):
    key = get_cache_key(data)
    r.set(key, json.dumps(result), ex=3600)