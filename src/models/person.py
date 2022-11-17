from uuid import UUID

from models.common import BaseOrjsonModel


class Person(BaseOrjsonModel):
    """
    Person model
    """
    id: UUID
    full_name: str
    role: list[str] | None
    films_id: list[UUID] | None
