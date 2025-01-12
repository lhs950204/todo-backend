from collections.abc import Generator
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from app.core.db import engine
from sqlmodel import SQLModel, delete
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(bind=engine) as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
