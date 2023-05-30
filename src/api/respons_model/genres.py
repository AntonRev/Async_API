from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GenreBasic(BaseModel):
    id: UUID
    name: str


class Genre(GenreBasic):
    description: Optional[str]

