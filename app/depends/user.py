from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlmodel import select

from app.core.security import verify_token
from app.depends.db import SessionDep
from app.depends.token import get_token_from_header
from app.models.user import User


def get_user_id(token: str = Depends(get_token_from_header)) -> UUID:
    payload = verify_token(token)
    return UUID(payload["sub"])


def get_user(session: SessionDep, token: str = Depends(get_token_from_header)) -> User:
    payload = verify_token(token)
    user = session.exec(select(User).where(User.id == UUID(payload["sub"]))).one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


UserDepends = Annotated[User, Depends(get_user)]
UserIDDepends = Annotated[UUID, Depends(get_user_id)]
