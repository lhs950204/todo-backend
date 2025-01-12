from pydantic import EmailStr
from sqlmodel import SQLModel


class UserRegisterSchema(SQLModel):
    email: EmailStr
    name: str
    password: str
