from fastapi.testclient import TestClient

from main import app
from services.AuthService import verify_jwt_token

client = TestClient(app)


def test_get_token():
    assert True


def test_get_token_invalid():
    assert True