from typing import Optional
from uuid import UUID

from models.common import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    """
    Movie genre model
    """
    id: UUID
    name: str
    description: Optional[str]


