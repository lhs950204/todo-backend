import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.note import Note
from app.models.user import User
from app.models.goal import Goal
from app.models.todo import Todo


@pytest.fixture
def default_note(session: Session, default_user: User, default_goal: Goal, default_todo: Todo) -> Note:
    note = Note(
        title="테스트 노트",
        content="테스트 내용",
        link_url="https://example.com",
        user_id=default_user.id,
        goal_id=default_goal.id,
        todo_id=default_todo.id,
    )
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


async def test_create_note(client: TestClient, login_user, default_goal: Goal, default_todo: Todo):
    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={
            "title": "새로운 노트",
            "content": "노트 내용",
            "link_url": "https://example.com",
            "goal_id": default_goal.id,
            "todo_id": default_todo.id,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "새로운 노트"
    assert response.json()["content"] == "노트 내용"
    assert "id" in response.json()


async def test_get_notes(client: TestClient, login_user, default_note: Note, default_goal: Goal):
    response = client.get(
        f"/notes?goal_id={default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["total_count"] == 1
    assert len(response.json()["notes"]) == 1
    assert response.json()["notes"][0]["title"] == "테스트 노트"
    assert response.json()["next_cursor"] is None


async def test_get_notes_with_cursor(
    client: TestClient, login_user, session: Session, default_user: User, default_goal: Goal, default_todo: Todo
):
    # 여러 개의 노트 생성
    notes = []
    for i in range(25):
        note = Note(
            title=f"노트 {i}",
            content=f"내용 {i}",
            link_url="https://example.com",
            user_id=default_user.id,
            goal_id=default_goal.id,
            todo_id=default_todo.id,
        )
        session.add(note)
        notes.append(note)
    session.commit()

    # 첫 페이지 요청
    response = client.get(
        f"/notes?goal_id={default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()["notes"]) == 20
    assert response.json()["next_cursor"] is not None

    # 다음 페이지 요청
    response = client.get(
        f"/notes?goal_id={default_goal.id}&cursor={response.json()['next_cursor']}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()["notes"]) == 5
    assert response.json()["next_cursor"] is None


async def test_get_note(
    client: TestClient, login_user, default_note: Note, default_user: User, default_goal: Goal, default_todo: Todo
):
    response = client.get(
        f"/notes/{default_note.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "테스트 노트"
    assert response.json()["content"] == "테스트 내용"
    assert response.json()["link_url"] == "https://example.com"
    assert response.json()["user_id"] == default_user.id
    assert response.json()["goal_id"] == default_goal.id
    assert response.json()["todo_id"] == default_todo.id
    assert response.json()["todo"]["id"] == default_todo.id


async def test_get_note_not_found(client: TestClient, login_user):
    response = client.get(
        "/notes/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 404


async def test_update_note(client: TestClient, login_user, default_note: Note):
    response = client.patch(
        f"/notes/{default_note.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "수정된 노트", "content": "수정된 내용"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "수정된 노트"
    assert response.json()["content"] == "수정된 내용"


async def test_update_note_not_found(client: TestClient, login_user):
    response = client.patch(
        "/notes/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "수정된 노트"},
    )
    assert response.status_code == 404


async def test_delete_note(client: TestClient, login_user, default_note: Note):
    response = client.delete(
        f"/notes/{default_note.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 204


async def test_delete_note_not_found(client: TestClient, login_user):
    response = client.delete(
        "/notes/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 404


async def test_create_note_with_invalid_goal(client: TestClient, login_user, session: Session, default_todo: Todo):
    # 다른 사용자의 goal 생성
    other_user = User(email="other@example.com", name="other", hashed_password="test")
    session.add(other_user)
    session.commit()

    other_goal = Goal(title="다른 사용자의 목표", user_id=other_user.id)
    session.add(other_goal)
    session.commit()

    response = client.post(
        "/notes",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={
            "title": "새로운 노트",
            "content": "노트 내용",
            "link_url": "https://example.com",
            "goal_id": other_goal.id,
            "todo_id": default_todo.id,
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Goal not found"
