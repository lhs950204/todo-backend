from typing import TYPE_CHECKING

from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.models.base import ModelBase
from app.models.goal import Goal

if TYPE_CHECKING:
    from app.models.todo import Todo


class User(ModelBase, table=True):
    email: EmailStr = Field(unique=True, index=True)
    name: str
    hashed_password: str

    goals: list["Goal"] = Relationship(back_populates="user")
    todos: list["Todo"] = Relationship(back_populates="user")
