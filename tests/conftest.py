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
from app.models.note import Note
from app.models.goal import Goal
from app.models.todo import Todo


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


@pytest.fixture()
def default_goal(session: Session, default_user: User):
    goal = Goal(title="테스트 목표", user_id=default_user.id)
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


@pytest.fixture()
def default_todo(session: Session, default_goal: Goal):
    todo = Todo(
        title="테스트 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        goal_id=default_goal.id,
        user_id=default_goal.user_id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


@pytest.fixture()
def default_note(session: Session, default_user: User, default_goal: Goal, default_todo: Todo):
    note = Note(
        title="테스트 노트",
        content="테스트 노트 내용",
        link_url="https://example.com",
        user_id=default_user.id,
        goal_id=default_goal.id,
        todo_id=default_todo.id,
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note
