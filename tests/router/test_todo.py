import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.models.user import User
from app.models.goal import Goal


@pytest.fixture
def default_todo(session: Session, default_user: User, default_goal: Goal) -> Todo:
    todo = Todo(
        title="테스트 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        user_id=default_user.id,
        goal_id=default_goal.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo


async def test_create_todo(client: TestClient, login_user, default_goal: Goal):
    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={
            "title": "새로운 할일",
            "linkUrl": "https://example.com",
            "fileUrl": "https://example.com/file",
            "goalId": default_goal.id,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "새로운 할일"
    assert "id" in response.json()


async def test_get_todos(client: TestClient, login_user, default_todo: Todo, default_goal: Goal):
    response = client.get(
        f"/todos?goalId={default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["total_count"] == 1
    assert len(response.json()["todos"]) == 1
    assert response.json()["todos"][0]["title"] == "테스트 할일"
    assert response.json()["next_cursor"] is None


async def test_get_todos_with_done_filter(
    client: TestClient, login_user, session: Session, default_user: User, default_goal: Goal
):
    # 완료된/미완료된 할일 생성
    todo1 = Todo(
        title="완료된 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        user_id=default_user.id,
        goal_id=default_goal.id,
        done=True,
    )
    todo2 = Todo(
        title="미완료된 할일",
        link_url="https://example.com",
        file_url="https://example.com/file",
        user_id=default_user.id,
        goal_id=default_goal.id,
        done=False,
    )
    session.add(todo1)
    session.add(todo2)
    session.commit()

    # 완료된 할일만 조회
    response = client.get(
        f"/todos?goalId={default_goal.id}&done=true",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 1
    assert response.json()["todos"][0]["title"] == "완료된 할일"

    # 미완료된 할일만 조회
    response = client.get(
        f"/todos?goalId={default_goal.id}&done=false",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()["todos"]) == 1
    assert response.json()["todos"][0]["title"] == "미완료된 할일"


async def test_get_todo_progress(
    client: TestClient, login_user, session: Session, default_user: User, default_goal: Goal
):
    # 완료된/미완료된 할일 생성
    todos = [
        Todo(
            title=f"할일 {i}",
            link_url="https://example.com",
            file_url="https://example.com/file",
            user_id=default_user.id,
            goal_id=default_goal.id,
            done=i < 2,  # 2개는 완료, 3개는 미완료
        )
        for i in range(5)
    ]
    session.add_all(todos)
    session.commit()

    response = client.get(
        f"/todos/progress?goalId={default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["progress"] == 0.4


async def test_get_todo(client: TestClient, login_user, default_todo: Todo):
    response = client.get(
        f"/todos/{default_todo.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "테스트 할일"


async def test_get_todo_not_found(client: TestClient, login_user):
    response = client.get(
        "/todos/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 404


async def test_update_todo(client: TestClient, login_user, default_todo: Todo):
    response = client.patch(
        f"/todos/{default_todo.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "수정된 할일", "done": True},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "수정된 할일"
    assert response.json()["done"] is True


async def test_update_todo_not_found(client: TestClient, login_user):
    response = client.patch(
        "/todos/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "수정된 할일"},
    )
    assert response.status_code == 404


async def test_delete_todo(client: TestClient, login_user, default_todo: Todo):
    response = client.delete(
        f"/todos/{default_todo.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 204


async def test_delete_todo_not_found(client: TestClient, login_user):
    response = client.delete(
        "/todos/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 404


async def test_create_todo_with_invalid_goal(client: TestClient, login_user, session: Session):
    # 다른 사용자의 goal 생성
    other_user = User(email="other@example.com", name="other", hashed_password="test")
    session.add(other_user)
    session.commit()

    other_goal = Goal(title="다른 사용자의 목표", user_id=other_user.id)
    session.add(other_goal)
    session.commit()

    response = client.post(
        "/todos",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={
            "title": "새로운 할일",
            "linkUrl": "https://example.com",
            "fileUrl": "https://example.com/file",
            "goalId": other_goal.id,
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"


async def test_update_todo_with_invalid_goal(client: TestClient, login_user, default_todo: Todo, session: Session):
    # 다른 사용자의 goal 생성
    other_user = User(email="other@example.com", name="other", hashed_password="test")
    session.add(other_user)
    session.commit()

    other_goal = Goal(title="다른 사용자의 목표", user_id=other_user.id)
    session.add(other_goal)
    session.commit()

    response = client.patch(
        f"/todos/{default_todo.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"goalId": other_goal.id},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"
