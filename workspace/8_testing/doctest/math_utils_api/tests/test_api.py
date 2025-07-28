"""
Tests for the FastAPI endpoints using pytest.
"""

import pytest
from fastapi.testclient import TestClient

# Use a relative import that works with the project structure
from app.api import app


@pytest.fixture
def client():
    """
    Pytest fixture to create a TestClient for the API.
    This makes the client available to all test functions that need it.
    """
    return TestClient(app)


@pytest.mark.parametrize(
    "endpoint, a, b, expected_status, expected_result",
    [
        # Test successful operations
        ("add", 2, 3, 200, {"result": 5}),
        ("subtract", 5, 3, 200, {"result": 2}),
        ("multiply", 2, 3, 200, {"result": 6}),
        ("divide", 6, 3, 200, {"result": 2.0}),
        # Test division by zero
        ("divide", 10, 0, 400, {"detail": "Cannot divide by zero"}),
    ],
)
def test_math_endpoints(client, endpoint, a, b, expected_status, expected_result):
    """
    Test the math endpoints with various inputs using pytest's parametrization.
    This single test covers multiple success and error cases.
    """
    response = client.post(f"/{endpoint}", json={"a": a, "b": b})
    assert response.status_code == expected_status
    assert response.json() == expected_result


def test_invalid_input_type(client):
    """
    Test the API's response to an invalid input type.
    FastAPI should return a 422 Unprocessable Entity error.
    """
    response = client.post("/add", json={"a": "invalid", "b": 3})
    assert response.status_code == 422


@pytest.mark.parametrize(
    "endpoint, a, b",
    [
        ("add", float("inf"), 1),
        ("subtract", 1, float("-inf")),
        ("multiply", float("inf"), float("-inf")),
        ("divide", 1, float("inf")),
    ],
)
def test_non_finite_numbers(client, endpoint, a, b):
    """
    Test that the API correctly handles non-finite numbers,
    which should be caught by the Pydantic model's validator.
    """
    response = client.post(f"/{endpoint}", json={"a": a, "b": b})
    assert response.status_code == 422  # Validation error
    # The exact error message can vary, so we check for the presence of key details
    assert "detail" in response.json()
    assert "finite" in response.text
