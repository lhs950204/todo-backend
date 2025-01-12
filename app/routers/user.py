from fastapi import APIRouter

from app.core.security import get_password_hash
from app.depends.db import SessionDep
from app.depends.user import UserDepends
from app.models.user import User
from app.schema.user import UserRegisterSchema

router = APIRouter(prefix="/user")


@router.post("", response_model=User, response_model_exclude={"hashed_password"})
async def register_user(user_in: UserRegisterSchema, session: SessionDep):
    user = User.model_validate(user_in, update={"hashed_password": get_password_hash(user_in.password)})
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("", response_model=User, response_model_exclude={"hashed_password"})
async def get_user(user: UserDepends):
    return user
