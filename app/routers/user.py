from fastapi import APIRouter

from app.core.security import get_password_hash
from app.models.user import User
from app.schema.user import UserRegisterSchema

router = APIRouter(prefix="/user")


@router.post("", response_model=User, response_model_exclude={"hashed_password"})
async def register_user(user_in: UserRegisterSchema):
    user = User.model_validate(user_in, update={"hashed_password": get_password_hash(user_in.password)})
    # TODO: save user to db
    # TODO: check duplicate email
    return user


@router.get("", response_model=User, response_model_exclude={"hashed_password"})
async def get_user(user_id: int):
    raise
