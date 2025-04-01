from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.note import Note
    from app.models.user import User


class Todo(ModelBase, table=True):
    title: str
    done: bool = Field(default=False)
    link_url: str | None = None
    file_url: str | None = None

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="todos")

    goal_id: int = Field(foreign_key="goal.id", nullable=False)
    goal: "Goal" = Relationship(back_populates="todos")

    note_id: int = Field(foreign_key="note.id", nullable=True)
    note: "Note" = Relationship(back_populates="todo")
