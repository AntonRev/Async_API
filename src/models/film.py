from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from models.common import BaseOrjsonModel


class PersonInfo(BaseOrjsonModel):
    """
    Basic information about a person (director / actor / writer)
    """
    id: UUID
    name: str


class Film(BaseOrjsonModel):
    """
    Film model (TV series or movie)
    """
    id: UUID
    imdb_rating: Optional[float]
    genre: list[str]
    title: str
    description: Optional[str]
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    actors: list[PersonInfo]
    writers: list[PersonInfo]
