from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class PersonInfo(BaseModel):
    """
    Basic person view model (nested model for film view models)
    """
    id: UUID
    name: str


class FilmBasic(BaseModel):
    """
    Basic film view model (for films list)
    """
    id: UUID
    title: str
    imdb_rating: Optional[float]


class Film(FilmBasic):
    """
    Film view model (for film details)
    """
    genre: list[str]
    description: Optional[str]
    director: list[str]
    actors: list[PersonInfo]
    writers: list[PersonInfo]