from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.user import User


class Goal(ModelBase, table=True):
    title: str

    user_id: int = Field(foreign_key="user.id")
    user: "User" = Relationship(back_populates="goals")
