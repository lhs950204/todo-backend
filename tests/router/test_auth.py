from fastapi.testclient import TestClient
from app.models.user import User


def test_login(client: TestClient, default_user: User):
    response = client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "test"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["name"] == "test"
    assert "hashed_password" not in response.json()
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


def test_refresh_token(client: TestClient, login_user):
    response = client.post(
        "/auth/tokens",
        headers={"Authorization": f"Bearer {login_user['refresh_token']}"},
    )
    assert response.status_code == 200
