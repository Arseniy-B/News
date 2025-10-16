from fastapi.responses import JSONResponse
from functools import wraps
from src.infrastructure.services.redis.redis import redis_helper
from redis.asyncio.client import Redis
import hashlib
import pickle
from pydantic import BaseModel


def args_kwargs_to_str(args, kwargs) -> str:
    def _convert(obj):
        if isinstance(obj, BaseModel):
            return str(obj.model_dump())
        if isinstance(obj, (list, tuple, set)):
            return str([_convert(i) for i in obj])
        if isinstance(obj, dict):
            return str({k: _convert(v) for k, v in obj.items()})
        return str(obj)

    return _convert({"args": args, "kwargs": kwargs})


def get_hash(*args, **kwargs):
    hash = hashlib.sha256(
        args_kwargs_to_str(args, kwargs).encode()
    ).hexdigest()
    return hash


def cache(ex):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            redis: Redis = await redis_helper.get_redis()
            key = f"{func.__name__}:{get_hash(*args, **kwargs)}"
            find_data = await redis.get(key)
            if find_data:
                return pickle.loads(find_data)
            res = await func(*args, **kwargs)
            await redis.set(key, pickle.dumps(res), ex=ex)
            return res
        return wrapper
    return decorator
