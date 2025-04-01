from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.note import Note
    from app.models.todo import Todo
    from app.models.user import User


class Goal(ModelBase):
    __tablename__ = "goal"

    title: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="goals")

    todos: Mapped[List["Todo"]] = relationship(back_populates="goal", lazy="selectin")
    notes: Mapped[List["Note"]] = relationship(back_populates="goal", lazy="selectin")
