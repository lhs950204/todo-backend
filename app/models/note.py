from typing import Optional

from sqlmodel import Field, Relationship

from app.models.base import ModelBase
from app.models.goal import Goal
from app.models.todo import Todo
from app.models.user import User


class NoteBase(ModelBase):
    title: str
    content: str
    link_url: Optional[str] = Field(default=None, nullable=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    goal_id: int = Field(foreign_key="goal.id", nullable=False)
    todo_id: int = Field(foreign_key="todo.id", nullable=False)


class Note(NoteBase, table=True):
    user: "User" = Relationship(back_populates="notes", sa_relationship_kwargs={"lazy": "selectin"})
    goal: "Goal" = Relationship(back_populates="notes", sa_relationship_kwargs={"lazy": "selectin"})
    todo: "Todo" = Relationship(back_populates="note", sa_relationship_kwargs={"lazy": "selectin"})
