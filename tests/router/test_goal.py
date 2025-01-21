import pytest
from fastapi.testclient import TestClient

from app.models.goal import Goal
from app.models.user import User
from sqlmodel import Session


@pytest.fixture
def default_goal(session: Session, default_user: User) -> Goal:
    goal = Goal(title="테스트 목표", user_id=default_user.id)
    session.add(goal)
    session.commit()
    session.refresh(goal)
    return goal


async def test_create_goal(client: TestClient, login_user):
    response = client.post(
        "/goals",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "새로운 목표"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "새로운 목표"
    assert "id" in response.json()


async def test_get_goals(client: TestClient, login_user, default_goal: Goal):
    response = client.get(
        "/goals",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["total_count"] == 1
    assert len(response.json()["goals"]) == 1
    assert response.json()["goals"][0]["title"] == "테스트 목표"
    assert response.json()["next_cursor"] is None


async def test_get_goals_with_cursor(client: TestClient, login_user, session: Session, default_user: User):
    # 여러 개의 목표 생성
    goals = []
    for i in range(25):  # size(20)보다 많은 데이터 생성
        goal = Goal(title=f"목표 {i}", user_id=default_user.id)
        session.add(goal)
        goals.append(goal)
    session.commit()

    # 첫 페이지 요청
    response = client.get(
        "/goals",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()["goals"]) == 20
    assert response.json()["next_cursor"] > 0

    # 다음 페이지 요청
    response = client.get(
        f"/goals?cursor={response.json()['next_cursor']}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json()["goals"]) == 5
    assert response.json()["next_cursor"] is None


async def test_get_goal(client: TestClient, login_user, default_goal: Goal):
    response = client.get(
        f"/goals/{default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "테스트 목표"


async def test_get_goal_not_found(client: TestClient, login_user):
    response = client.get(
        "/goals/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 404


async def test_update_goal(client: TestClient, login_user, default_goal: Goal):
    response = client.patch(
        f"/goals/{default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "수정된 목표"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "수정된 목표"


async def test_update_goal_not_found(client: TestClient, login_user):
    response = client.patch(
        "/goals/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
        json={"title": "수정된 목표"},
    )
    assert response.status_code == 404


async def test_delete_goal(client: TestClient, login_user, default_goal: Goal):
    response = client.delete(
        f"/goals/{default_goal.id}",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 204


async def test_delete_goal_not_found(client: TestClient, login_user):
    response = client.delete(
        "/goals/999999",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 404


async def test_get_goals_with_sort_order(client: TestClient, login_user, session: Session, default_user: User):
    # 여러 개의 목표 생성
    goals = []
    for i in range(3):
        goal = Goal(title=f"목표 {i}", user_id=default_user.id)
        session.add(goal)
        goals.append(goal)
    session.commit()

    # 내림차순 정렬 (기본값)
    response = client.get(
        "/goals",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["goals"][0]["title"] == "목표 2"
    assert response.json()["goals"][-1]["title"] == "목표 0"

    # 오름차순 정렬
    response = client.get(
        "/goals?sortOrder=oldest",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["goals"][0]["title"] == "목표 0"
    assert response.json()["goals"][-1]["title"] == "목표 2"
