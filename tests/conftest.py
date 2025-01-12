from collections.abc import Generator
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from app.core.db import engine
from sqlmodel import SQLModel, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.depends.db import SessionDep
from app.main import app
from app.models.user import User


@pytest.fixture(scope="session", autouse=True)
async def reset_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=engine) as session:
        try:
            print("db")
            yield session
        finally:
            await session.rollback()


app.dependency_overrides[SessionDep] = db


@pytest.fixture(scope="session")
async def default_user(db: AsyncSession):
    user = User(
        email="test@example.com",
        hashed_password="test",
        name="test",
    )
    db.add(user)
    await db.commit()
    return user


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
