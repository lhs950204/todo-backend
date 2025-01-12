from typing import Annotated

from fastapi import Depends

from app.depends.token import get_token_from_header
from app.models.user import User


def get_user(token: str = Depends(get_token_from_header)) -> User:
    raise


UserDepends = Annotated[User, Depends(get_user)]
