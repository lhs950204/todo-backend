from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr
    name: str
    password: str
