from fastapi.testclient import TestClient

from app.models.user import User


async def test_register_user(client: TestClient):
    response = client.post(
        "/user",
        json={
            "email": "test2@example.com",
            "password": "test",
            "name": "test",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test2@example.com"
    assert response.json()["name"] == "test"
    assert "hashed_password" not in response.json()


async def test_register_user_duplicate(client: TestClient, default_user: User):
    response = client.post(
        "/user",
        json={
            "email": "test@example.com",
            "password": "test",
            "name": "test",
        },
    )
    assert response.status_code == 400


async def test_get_user(client: TestClient, login_user):
    response = client.get(
        f"/user",
        headers={"Authorization": f"Bearer {login_user['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["name"] == "test"
    assert "hashed_password" not in response.json()
