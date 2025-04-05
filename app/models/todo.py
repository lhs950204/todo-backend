from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.note import Note
    from app.models.user import User


class TodoBase(ModelBase):
    title: str
    done: bool = Field(default=False)
    link_url: str | None = None
    file_url: str | None = None

    user_id: int = Field(foreign_key="user.id", nullable=False)
    goal_id: int = Field(foreign_key="goal.id", nullable=False)


class Todo(TodoBase, table=True):
    user: "User" = Relationship(back_populates="todos")

    goal: "Goal" = Relationship(back_populates="todos")

    note: "Note" = Relationship(back_populates="todo", sa_relationship_kwargs={"uselist": False, "lazy": "selectin"})

    @property
    def note_id(self) -> int | None:
        return self.note.id if self.note else None
