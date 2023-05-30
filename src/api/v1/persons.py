from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query

from api.respons_model.persons import PersonBase, Person
from api.v1.common import QueryStr, Sorting, get_parameters
from api.v1.message_texts import MessageText
from services.persons import PersonService, get_service

router = APIRouter()


@router.get('/', response_model=list[PersonBase],
            summary="Выдача всех актеров",
            description="Все актеры",
            response_description="Полное имя и ID")
async def person_list(query: QueryStr = Depends(get_parameters),
                      person_service: PersonService = Depends(get_service)) -> list[PersonBase]:
    persons = await person_service.get_all(query)
    return [PersonBase(**p.dict()) for p in persons]


@router.get('/search', response_model=list[PersonBase],
            summary="Поиск по актёрам",
            description="Полнотекстовый поиск по актёрам",
            response_description="Полное имя и ID")
async def person_search_list(query: str,
                             page: int = Query(default=1, ge=1, le=10000, alias='page[number]'),
                             size: int = Query(default=10, ge=1, le=10000, alias='page[size]'),
                             sort: Optional[Sorting] = None,
                             person_service: PersonService = Depends(get_service)) -> list[PersonBase]:
    persons = await person_service.search(query, page, size, sort)
    return [PersonBase(**f.dict()) for f in persons]


@router.get('/{person_id}', response_model=Person,
            summary="Выдача актера по ID",
            description="Вся информация об актере",
            response_description="ID, полное имя, роль и фильмы в которых принимал участие актер")
async def person_details(person_id: UUID, person_service: PersonService = Depends(get_service)) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=MessageText.PERSON_NOT_FOUND)

    return Person(**person.dict())
