from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.v1.message_texts import MessageText
from services.JWT import get_role
from services.film import FilmService, FilmSorting, get_film_service
from api.respons_model.film import FilmBasic, Film
router = APIRouter()


@router.get('/',
            response_model=list[FilmBasic],
            summary="Список кинопроизведений",
            description="Список кинопроизведений, разбитый по страницам, опционально - отсортированный "
                        "и отфильтрованный по жанрам",
            response_description="Название и рейтинг фильма")
async def films_list(page: int = Query(default=1, ge=1, le=10000, alias='page[number]'),
                     size: int = Query(default=10, ge=1, le=10000, alias='page[size]'),
                     genre: Optional[str] = Query(default=None, alias='filter[genre]'),
                     sort: Optional[FilmSorting] = None,
                     roles: list = Depends(get_role),
                     film_service: FilmService = Depends(get_film_service)) -> list[FilmBasic]:
    films = await film_service.get_all(page, size, genre, sort, roles)
    return [FilmBasic(**f.dict()) for f in films]


@router.get('/search', response_model=list[FilmBasic],
            summary="Поиск кинопроизведений",
            description="Полнотекстовый поиск по кинопроизведениям",
            response_description="Название и рейтинг фильма")
async def films_search(query: str,
                       page: int = Query(default=1, ge=1, le=10000, alias='page[number]'),
                       size: int = Query(default=10, ge=1, le=10000, alias='page[size]'),
                       film_service: FilmService = Depends(get_film_service)) -> list[FilmBasic]:
    films = await film_service.search(query, page, size)
    return [FilmBasic(**f.dict()) for f in films]


@router.get('/{film_id}', response_model=Film,
            summary="Выдача фильма по ID",
            description="Кинопроизведение по ID",
            response_description="Полная информация о фильме")
async def film_details(film_id: UUID, film_service: FilmService = Depends(get_film_service)) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MessageText.FILM_NOT_FOUND)

    return Film(**film.dict())
