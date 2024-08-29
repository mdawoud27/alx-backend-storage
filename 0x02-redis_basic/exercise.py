#!/usr/bin/env python3
"""Python with Redis"""
import redis
import uuid
from typing import Union, Optional, Callable, Tuple, Dict
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that takes callable args and count how many times
    the Cache class are called
    """
    @wraps(method)
    def wrapper(self, *args: Tuple, **kwargs: Dict) -> Callable:
        """wrapped function """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    """Cache Class for redis connection"""

    def __init__(self) -> None:
        """Init redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Function that generate a random key"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> str:
        """Get the value of the entered key"""
        value = self._redis.get(key)

        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Convert entered key to string"""
        return self.get(key, lambda data: data.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Convert the entered key to integer"""
        return int(key)
