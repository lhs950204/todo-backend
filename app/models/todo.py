from sqlmodel import Field, Relationship

from app.models.base import ModelBase
from app.models.goal import Goal
from app.models.user import User


class Todo(ModelBase, table=True):
    title: str
    done: bool = Field(default=False)
    link_url: str
    file_url: str

    # note_id: int | None = Field(foreign_key="note.id")
    # note: "Note" = Relationship(back_populates="todos")

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="todos")

    goal_id: int = Field(foreign_key="goal.id", nullable=False)
    goal: "Goal" = Relationship(back_populates="todos")
