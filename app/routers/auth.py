from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import select

from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_token,
)
from app.depends.db import SessionDep
from app.depends.token import get_token_from_header
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", name="로그인")
async def login(session: SessionDep, email: str = Body(...), password: str = Body(...)):
    user = session.exec(select(User).where(User.email == email)).one_or_none()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 잘못되었습니다")

    return {
        **user.model_dump(exclude={"hashed_password"}),
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@router.post("/tokens", name="토큰 재발급")
async def refresh_token(session: SessionDep, token: str = Depends(get_token_from_header)):
    # 토큰 검증
    payload = verify_token(token)

    # refresh 토큰인지 확인
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid token type")

    # 사용자 확인
    user = session.exec(select(User).where(User.id == int(payload["sub"]))).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 새로운 토큰 발급
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }
