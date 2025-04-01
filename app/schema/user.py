from pydantic import BaseModel, EmailStr


class UserRegisterSchema(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserCreateSchema(BaseModel):
    email: EmailStr
    name: str
    hashed_password: str


class UserUpdateSchema(BaseModel):
    password: str


class UserSchema(UserCreateSchema):
    id: int
