from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.models.todo import Todo
from app.models.user import User


async def test_create_todo(session: Session, default_user: User):
    # Goal 생성
    goal = Goal(title="테스트 목표", user_id=default_user.id, user=default_user)
    session.add(goal)
    session.commit()
    session.refresh(goal)

    # Todo 생성
    todo = Todo(
        title="테스트 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        user_id=default_user.id,
        goal_id=goal.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # 검증
    assert todo.id is not None
    assert todo.title == "테스트 할일"
    assert todo.done is False  # 기본값 확인
    assert todo.link_url == "https://example.com"
    assert todo.file_url == "https://example.com/file"
    assert todo.user_id == default_user.id
    assert todo.goal_id == goal.id
    assert todo.created_at is not None
    assert todo.updated_at is not None


async def test_update_todo(session: Session, default_user: User):
    # Goal 생성
    goal = Goal(title="테스트 목표", user_id=default_user.id, user=default_user)
    session.add(goal)
    session.commit()

    # Todo 생성
    todo = Todo(
        title="테스트 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        user_id=default_user.id,
        goal_id=goal.id,
    )
    session.add(todo)
    session.commit()

    # Todo 업데이트
    todo.title = "수정된 할일"
    todo.done = True
    session.commit()
    session.refresh(todo)

    # 검증
    updated_todo = session.scalar(select(Todo).where(Todo.id == todo.id))
    assert updated_todo is not None
    assert updated_todo.title == "수정된 할일"
    assert updated_todo.done is True


async def test_todo_relationships(session: Session, default_user: User):
    # Goal 생성
    goal = Goal(title="테스트 목표", user_id=default_user.id, user=default_user)
    session.add(goal)
    session.commit()

    # Todo 생성
    todo = Todo(
        title="테스트 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        user_id=default_user.id,
        goal_id=goal.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    # 관계 검증
    assert todo.user.id == default_user.id
    assert todo.user.email == default_user.email
    assert todo.goal.id == goal.id
    assert todo.goal.title == "테스트 목표"

    assert len(default_user.todos) == 1
    assert default_user.todos[0].id == todo.id
    assert len(default_user.goals) == 1
    assert default_user.goals[0].id == goal.id
