import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


@pytest.mark.parametrize(
    "name,expected_message",
    [
        ("jay", "Hello, jay!"),
        ("Alice", "Hello, Alice!"),
        ("Bob", "Hello, Bob!"),
    ]
)
def test_greet_user(client, name, expected_message):
    response = client.get(f"/greet/{name}")
    assert response.status_code == 200
    assert response.json() == {"message": expected_message}


def test_greet_user_require_name(client):
    response = client.get("/greet/")
    assert response.status_code == 404
