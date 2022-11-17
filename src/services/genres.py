from functools import lru_cache
from typing import Optional
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from api.v1.common import QueryStr, Sorting
from core.configs import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from services.redis_heplers import RedisHelper

CACHE_EXPIRE_IN_SECONDS = config.CACHE_EXPIRE_IN_SECONDS
ELASTIC_INDEX = 'genres'


class GenreService:
    """
    Service to get genre(get all, get by id, search by query string).
    Uses Elastic as a database and Redis as a cache.
    """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.redis_helper = RedisHelper(self.redis)

    async def get_all(self, query: QueryStr = None) -> list[Genre]:
        genres = await self.redis_helper.get_from_cache_or_db(
            key=f'genres_all:{query.page_number}_{query.page_size}_{query.sort}',
            get_from_db=lambda: self._get_all_from_elastic(query),
            parse_raw=Genre.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )

        return genres

    async def _get_all_from_elastic(self, query: QueryStr = None) -> list[Genre]:
        order = "desc" if query.sort == Sorting.NAME_DESC else "asc"
        sort = [
            {
                "name.raw": {
                    "unmapped_type": "keyword",
                    "order": order
                }
            }
        ]
        docs = await self.elastic.search(
            index=ELASTIC_INDEX,
            body={'sort': sort},
            q='*',
            from_=(query.page_number - 1) * query.page_size,
            size=query.page_size,
        )
        return [Genre(**d['_source']) for d in docs['hits']['hits']]

    async def get_by_id(self, genre_id: UUID) -> Optional[Genre]:
        genre = await self.redis_helper.get_from_cache_or_db(
            key=f'genre:{genre_id}',
            get_from_db=lambda: self._get_from_elastic(genre_id),
            parse_raw=Genre.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )

        return genre

    async def _get_from_elastic(self, genre_id: UUID) -> Optional[Genre]:
        try:
            doc = await self.elastic.get(index=ELASTIC_INDEX, id=genre_id)
        except NotFoundError:
            return None
        return Genre(**doc['_source'])


@lru_cache()
def get_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(redis, elastic)
