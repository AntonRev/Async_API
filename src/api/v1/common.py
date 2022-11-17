from enum import Enum

from fastapi import Query
from pydantic import BaseModel


class Sorting(str, Enum):
    NAME = 'a-z'
    NAME_DESC = 'z-a'


class QueryStr(BaseModel):
    sort: Sorting
    page_size: int
    page_number: int


def get_parameters(_page_size: int = Query(10, ge=1, alias='page[size]'),
                   _page_number: int = Query(1, ge=1, alias='page[number]'),
                   _sort: Sorting = Query(Sorting.NAME, alias='sort')):
    return QueryStr(page_size=_page_size, sort=_sort, page_number=_page_number)
