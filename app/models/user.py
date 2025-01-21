from pydantic import EmailStr
from sqlmodel import Field, Relationship

from app.models.base import ModelBase
from app.models.goal import Goal


class User(ModelBase, table=True):
    email: EmailStr = Field(unique=True, index=True)
    name: str
    hashed_password: str

    goals: list["Goal"] = Relationship(back_populates="user")
