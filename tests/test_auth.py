from fastapi.testclient import TestClient

from main import app
from services.AuthService import verify_jwt_token

client = TestClient(app)


def test_get_token():
    response = client.post("/auth", json={"login": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    token = response.json()["access_token"]
    decoded_data = verify_jwt_token(token)
    assert decoded_data is not None

    return token


def test_get_token_invalid():
    response = client.post("/auth", json={"login": "valera", "password": "valera"})
    assert response.status_code == 400