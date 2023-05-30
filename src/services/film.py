from enum import Enum
from functools import lru_cache
from typing import Optional
from uuid import UUID

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from configs.configs import config
from db.elastic import get_elastic
from db.redis import get_redis
from models.film import Film
from services.redis_heplers import RedisHelper

CACHE_EXPIRE_IN_SECONDS = config.CACHE_EXPIRE_IN_SECONDS
ELASTIC_INDEX = 'movies'


class FilmSorting(str, Enum):
    """
    Film sorting options.
    Minus sign means "descending".
    If the field has nested text/keyword type - add ".raw" to field to sort by keyword, not text.
    """
    ID = 'id'
    ID_DESC = '-id'
    RATING = 'imdb_rating'
    RATING_DESC = '-imdb_rating'
    TITLE = 'title'
    TITLE_DESC = '-title'

    def to_elastic(self):
        if self.value[0] == '-':
            field = self.value[1:]
            order = 'desc'
        else:
            field = self.value
            order = 'asc'

        if field == 'title':
            field += '.raw'

        return {field: order}


class FilmService:
    """
    Service to get movies (get all, get by id, search by query string).
    Uses Elastic as a database and Redis as a cache.
    """

    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic
        self.redis_helper = RedisHelper(self.redis)

    async def get_all(self, page: int, page_size: int, roles: list, genre: Optional[str] = None,
                      sort_by: Optional[FilmSorting] = None) -> list[Film]:
        """
        Get movies list, paginated and, optionally, filtered by genre and sorted
        :param page: page number
        :param page_size: page size
        :param genre: genre name (case sensitive)
        :param sort_by: sorting (enum)
        :return: list of films
        """
        films = await self.redis_helper.get_from_cache_or_db(
            key=f'films_all:{page}_{page_size}_{genre}_{sort_by}',
            get_from_db=lambda: self._get_films_from_elastic(page, page_size, genre, sort_by),
            parse_raw=Film.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )
        if 'user' in roles:
            return films
        return films[:20]

    async def _get_films_from_elastic(self, page: int, page_size: int, genre: Optional[str],
                                      sort_by: Optional[FilmSorting]) -> list[Film]:
        if genre:
            query = {
                'bool': {
                    'filter': [
                        {
                            'term': {'genre': genre}
                        }
                    ]
                }
            }
        else:
            query = {
                'match_all': {}
            }

        docs = await self.elastic.search(
            index=ELASTIC_INDEX,
            body={'query': query, 'sort': [sort_by.to_elastic()] if sort_by else []},
            from_=(page - 1) * page_size,
            size=page_size,
        )
        return [Film(**d['_source']) for d in docs['hits']['hits']]

    async def search(self, query: str, page: int, page_size: int) -> list[Film]:
        """
        Search film by query string
        :param query: query string
        :param page: page number
        :param page_size: page size
        :return: list of films
        """
        films = await self.redis_helper.get_from_cache_or_db(
            key=f'films_search:{query}_{page}_{page_size}',
            get_from_db=lambda: self._search_films_in_elastic(query, page, page_size),
            parse_raw=Film.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )
        return films

    async def _search_films_in_elastic(self, query: str, page: int, page_size: int) -> list[Film]:
        docs = await self.elastic.search(
            index=ELASTIC_INDEX,
            body={'query': {'query_string': {'query': query}}},
            from_=(page - 1) * page_size,
            size=page_size,
        )
        return [Film(**d['_source']) for d in docs['hits']['hits']]

    async def get_by_id(self, film_id: UUID) -> Optional[Film]:
        """
        Get film by ID (or None if not found)
        :param film_id: ID (UUID)
        :return: Film or None
        """

        film = await self.redis_helper.get_from_cache_or_db(
            key=f'film:{film_id}',
            get_from_db=lambda: self._get_film_from_elastic(film_id),
            parse_raw=Film.parse_raw,
            expire=CACHE_EXPIRE_IN_SECONDS
        )
        return film

    async def _get_film_from_elastic(self, film_id: UUID) -> Optional[Film]:
        try:
            doc = await self.elastic.get(ELASTIC_INDEX, film_id)
        except NotFoundError:
            return None
        return Film(**doc['_source'])


@lru_cache()
def get_film_service(
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
