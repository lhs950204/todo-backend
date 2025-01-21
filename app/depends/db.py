from typing import Annotated, Generator

from fastapi import Depends
from sqlmodel import Session

from app.core.db import engine


def get_db() -> Generator[Session, None, None]:
    with Session(bind=engine, expire_on_commit=False) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
