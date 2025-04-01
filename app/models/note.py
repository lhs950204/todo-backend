from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.todo import Todo
    from app.models.user import User


class Note(ModelBase):
    __tablename__ = "note"

    title: Mapped[str]
    content: Mapped[str]
    link_url: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="notes")

    goal_id: Mapped[int] = mapped_column(ForeignKey("goal.id"), nullable=False)
    goal: Mapped["Goal"] = relationship(back_populates="notes")

    todo_id: Mapped[int] = mapped_column(ForeignKey("todo.id"), nullable=False)
    todo: Mapped["Todo"] = relationship(back_populates="note")
