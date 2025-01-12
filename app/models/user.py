from pydantic import EmailStr
from sqlmodel import Field

from app.models.base import ModelBase


class User(ModelBase):
    email: EmailStr = Field(unique=True, index=True)
    name: str
    hashed_password: str
