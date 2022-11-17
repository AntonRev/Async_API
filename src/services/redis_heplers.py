import json
from typing import Callable, Optional, TypeVar

from aioredis import Redis
from pydantic import BaseModel

ModelT = TypeVar('ModelT', bound=BaseModel)


class RedisHelper:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def _from_cache(self, key: str, parse_raw: Callable) -> Optional[ModelT | list[ModelT]]:
        data = await self.redis.get(key, encoding='UTF-8')
        if not data:
            return None

        if data.startswith('['):
            items = json.loads(data)
            result = [parse_raw(item) for item in items]
        else:
            result = parse_raw(data)
        return result

    async def _put_to_cache(self, key: str, content: ModelT | list[ModelT], expire: int) -> None:
        if isinstance(content, list):
            value = json.dumps([item.json() for item in content])
        else:
            value = content.json()

        await self.redis.set(key, value, expire=expire)

    async def get_from_cache_or_db(self, key: str, get_from_db: Callable, parse_raw: Callable,
                                   expire: int) -> Optional[ModelT | list[ModelT]]:
        """
        Get and item of list of items from cache or db
        :param key: redis key
        :param get_from_db: callable to get results from db
        :param parse_raw: callable to get parse a model from string
        :param expire: cache expire in seconds
        :return: model of list of models or None
        """
        result = await self._from_cache(key, parse_raw)
        if result is None:
            result = await get_from_db()
            if result is None:
                return None
            await self._put_to_cache(key, result, expire)

        return result
