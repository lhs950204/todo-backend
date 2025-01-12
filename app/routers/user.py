from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.security import get_password_hash
from app.depends.db import SessionDep
from app.depends.user import UserDepends
from app.models.user import User
from app.schema.user import UserRegisterSchema

router = APIRouter(prefix="/user")


@router.post("", response_model=User, response_model_exclude={"hashed_password"})
async def register_user(user_in: UserRegisterSchema, session: SessionDep):
    user = (await session.exec(select(User).where(User.email == user_in.email))).first()
    if user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user = User.model_validate(user_in, update={"hashed_password": get_password_hash(user_in.password)})
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("", response_model=User, response_model_exclude={"hashed_password"})
async def get_user(user: UserDepends):
    return user
