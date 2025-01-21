from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import ModelBase
from app.models.goal import Goal
from app.models.todo import Todo
from app.models.user import User


class Note(ModelBase, table=True):
    title: str
    content: str
    link_url: str

    user_id: int = Field(foreign_key="user.id", nullable=False)
    user: "User" = Relationship(back_populates="notes")

    goal_id: int = Field(foreign_key="goal.id", nullable=False)
    goal: "Goal" = Relationship(back_populates="notes")

    todo_id: int = Field(foreign_key="todo.id", nullable=False)
    todo: "Todo" = Relationship(back_populates="note")
