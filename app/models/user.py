from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.goal import Goal
    from app.models.note import Note
    from app.models.todo import Todo


class User(ModelBase):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    name: Mapped[str]

    goals: Mapped[List["Goal"]] = relationship(back_populates="user", lazy="selectin")
    todos: Mapped[List["Todo"]] = relationship(back_populates="user", lazy="selectin")
    notes: Mapped[List["Note"]] = relationship(back_populates="user", lazy="selectin")
    files: Mapped[List["File"]] = relationship(back_populates="user", lazy="selectin")
