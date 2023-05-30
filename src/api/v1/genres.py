from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from api.respons_model.genres import GenreBasic, Genre
from api.v1.common import QueryStr, get_parameters
from api.v1.message_texts import MessageText
from services.genres import GenreService, get_service

router = APIRouter()


@router.get('/', response_model=list[GenreBasic],
            summary="Выдача всех жанров",
            description="Все жанры",
            response_description="Название и ID")
async def genres_list(query: QueryStr = Depends(get_parameters),
                      genre_service: GenreService = Depends(get_service)) -> list[GenreBasic]:
    genres = await genre_service.get_all(query)
    return [GenreBasic(**g.dict()) for g in genres]


@router.get('/{genre_id}', response_model=Genre,
            summary="Выдача жанра по ID",
            description="Жанр по ID",
            response_description="Полная выдача информации о жанре")
async def genre_details(genre_id: UUID, genre_service: GenreService = Depends(get_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MessageText.GENRE_NOT_FOUND)

    return Genre(**genre.dict())
