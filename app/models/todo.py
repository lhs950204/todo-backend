from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.goal import Goal
    from app.models.note import Note
    from app.models.user import User


class Todo(ModelBase):
    __tablename__ = "todo"

    title: Mapped[str]
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    link_url: Mapped[Optional[str]]
    file_url: Mapped[Optional[str]]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="todos")

    goal_id: Mapped[int] = mapped_column(ForeignKey("goal.id"), nullable=False)
    goal: Mapped["Goal"] = relationship(back_populates="todos")

    note_id: Mapped[Optional[int]] = mapped_column(ForeignKey("note.id"), nullable=True)
    note: Mapped[Optional["Note"]] = relationship(back_populates="todo")
