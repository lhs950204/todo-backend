from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    # from app.models.note import Note
    from app.models.todo import Todo
    from app.models.user import User


class Goal(ModelBase, table=True):
    title: str

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="goals")

    todos: list["Todo"] = Relationship(back_populates="goal")
    # notes: List["Note"] = Relationship(back_populates="goal")
