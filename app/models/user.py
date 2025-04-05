from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.models.base import ModelBase

if TYPE_CHECKING:
    from app.models.file import File
    from app.models.goal import Goal
    from app.models.note import Note
    from app.models.todo import Todo


class UserBase(ModelBase):
    email: EmailStr = Field(unique=True)
    name: str


class User(UserBase, table=True):
    hashed_password: str

    goals: list["Goal"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    todos: list["Todo"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    notes: list["Note"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    files: list["File"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
