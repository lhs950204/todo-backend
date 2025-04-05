from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import ModelBase
from app.models.user import User

if TYPE_CHECKING:
    from app.models.note import Note
    from app.models.todo import Todo


class GoalBase(ModelBase):
    title: str
    user_id: int = Field(foreign_key="user.id", nullable=False)


class Goal(GoalBase, table=True):
    user: "User" = Relationship(back_populates="goals")
    todos: list["Todo"] = Relationship(back_populates="goal", sa_relationship_kwargs={"lazy": "selectin"})
    notes: list["Note"] = Relationship(back_populates="goal", sa_relationship_kwargs={"lazy": "selectin"})
