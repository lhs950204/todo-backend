from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.security import get_password_hash
from app.depends.db import SessionDep
from app.depends.user import UserDepends
from app.models.user import User, UserBase
from app.schema.user import UserRegisterSchema

router = APIRouter(prefix="/user", tags=["User"])


@router.post(
    "",
    name="회원 가입",
    response_model=UserBase,
    response_model_exclude={"hashed_password"},
)
async def register_user(user_in: UserRegisterSchema, session: SessionDep):
    user = session.exec(
        select(User).where(
            User.email == user_in.email,
        )
    ).first()
    if user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user = User.model_validate(user_in, update={"hashed_password": get_password_hash(user_in.password)})
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.get(
    "",
    name="회원정보 조회",
    response_model=UserBase,
    response_model_exclude={"hashed_password"},
)
async def get_user(user: UserDepends):
    return user
