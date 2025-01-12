from fastapi.testclient import TestClient


async def test_register_user(client: TestClient):
    response = client.post(
        "/user",
        json={
            "email": "test@example.com",
            "password": "test",
            "name": "test",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert response.json()["name"] == "test"
    assert "hashed_password" not in response.json()
