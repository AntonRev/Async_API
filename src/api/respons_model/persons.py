from uuid import UUID

from pydantic import BaseModel


class PersonBase(BaseModel):
    """
    Basic Person view model
    """
    id: UUID
    full_name: str


class Person(PersonBase):
    films_id: list[UUID] | None
    role: list[str] | None
