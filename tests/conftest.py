from typing import Generator

import pytest
from fastapi.testclient import TestClient
from app.core.db import engine
from sqlmodel import SQLModel, Session, select
import sqlalchemy as sa

from app.core.security import get_password_hash
from app.depends.db import SessionDep
from app.main import app
from app.models.user import User


@pytest.fixture(scope="function", autouse=True)
def reset_db():
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)


@pytest.fixture()
def session():
    with Session(bind=engine) as session:
        yield session


app.dependency_overrides[SessionDep] = session


@pytest.fixture(scope="function")
def default_user(session: Session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("test"),
        name="test",
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    # assert user.id is not None

    return user


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def login_user(client: TestClient, default_user: User):
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "test"},
    )
    return response.json()
