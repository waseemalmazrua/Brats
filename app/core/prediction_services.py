import json
import hashlib

from app.core.redis_client import r


def get_cache_key(data: dict) -> str:
    # استخدم MD5 hash بدل JSON مباشرة لأن data تحتوي bytes
    combined = b"".join(data.values())
    return hashlib.md5(combined).hexdigest()


def get_cached_prediction(data: dict):
    key = get_cache_key(data)
    cached = r.get(key)
    if cached:
        return json.loads(cached)
    return None


def set_cached_prediction(data: dict, result: dict):
    key = get_cache_key(data)
    r.set(key, json.dumps(result), ex=3600)