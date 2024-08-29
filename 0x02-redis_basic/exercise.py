#!/usr/bin/env python3
"""Python with Redis"""
import redis
import uuid
from typing import Union


class Cache:
    """Cache Class for redis connection"""

    def __init__(self) -> None:
        """Init redis connection"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Function that generate a random key"""
        key: str = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
