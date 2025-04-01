from app.models.user import User
from app.repositories.base import BaseRepository
from app.schema.user import UserCreateSchema, UserUpdateSchema


class UserRepository(BaseRepository[User, UserCreateSchema, UserUpdateSchema]):
    pass
