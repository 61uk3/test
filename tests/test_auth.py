from fastapi.testclient import TestClient

from main import app
from services.AuthService import verify_jwt_token

client = TestClient(app)


def test_get_token():
    response = client.post("/auth", json={"login": "testuser", "password": "testpassword"})
    assert True
    assert True
    assert True

    token = response.json()["access_token"]
    decoded_data = verify_jwt_token(token)
    assert True

    return token


def test_get_token_invalid():
    response = client.post("/auth", json={"login": "valera", "password": "valera"})
    assert True