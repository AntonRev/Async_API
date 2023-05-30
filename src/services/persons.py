from functools import lru_cache
from typing import Optional
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.common import QueryStr, Sorting
from configs.configs import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.person import Person
from services.redis_heplers import RedisHelper

CACHE_EXPIRE_IN_SECONDS = config.CACHE_EXPIRE_IN_SECONDS
ELASTIC_INDEX = 'persons'


class PersonService:
    """
    Service to get person (get all, get by id, search by query string).
    Uses Elastic as a database and Redis as a cache.
    """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.redis_helper = RedisHelper(self.redis)

    async def get_all(self, query: QueryStr = None) -> list[Person]:
        persons = await self.redis_helper.get_from_cache_or_db(
            key=f'persons_all:{query.page_number}_{query.page_size}_{query.sort}',
            get_from_db=lambda: self._get_all_from_elastic(query),
            parse_raw=Person.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )

        return persons

    async def search(self, query: str, page: int, page_size: int,
                     q_sort: Optional[Sorting.NAME_DESC] = None) -> list[Person]:
        order = "desc" if q_sort == Sorting.NAME_DESC else "asc"
        sort = [
            {
                "full_name.raw": {
                    "unmapped_type": "keyword",
                    "order": order
                }
            }
        ]
        docs = await self.elastic.search(
            index=ELASTIC_INDEX,
            body={'sort': sort},
            q=query,
            from_=(page - 1) * page_size,
            size=page_size,
        )
        return [Person(**d['_source']) for d in docs['hits']['hits']]

    async def _get_all_from_elastic(self, query: QueryStr = None) -> list[Person]:
        order = "desc" if query.sort == Sorting.NAME_DESC else "asc"
        sort = [
            {
                "full_name.raw": {
                    "unmapped_type": "keyword",
                    "order": order
                }
            }
        ]
        docs = await self.elastic.search(
            index=ELASTIC_INDEX,
            body={'sort': sort},
            q="*",
            from_=(query.page_number - 1) * query.page_size,
            size=query.page_size,
        )
        return [Person(**d['_source']) for d in docs['hits']['hits']]

    async def get_by_id(self, person_id: UUID) -> Optional[Person]:
        person = await self.redis_helper.get_from_cache_or_db(
            key=f'person:{person_id}',
            get_from_db=lambda: self._get_from_elastic(person_id),
            parse_raw=Person.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )

        return person

    async def _get_from_elastic(self, person_id: UUID) -> Optional[Person]:
        try:
            doc = await self.elastic.get(index=ELASTIC_INDEX, id=person_id)
        except NotFoundError:
            return None
        return Person(**doc['_source'])


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(redis, elastic)
