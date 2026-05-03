import hashlib
import json


def get_cache_key(data: dict) -> str:
    combined = json.dumps(data, sort_keys=True).encode()
    return hashlib.md5(combined).hexdigest()


def get_cached_prediction(data: dict):
    return None  # caching disabled


def set_cached_prediction(data: dict, result: dict):
    pass  # caching disabled