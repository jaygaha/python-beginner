"""
Test API endpoints for math_utils app.
"""

import pytest

from app.api import app


# @pytest.fixture: Sets up a test environment before each test.
@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()
    return client


def test_add_endpoint(client):
    response = client.post("/add", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json == {"result": 5}


def test_subtract_endpoint(client):
    response = client.post("/subtract", json={"a": 5, "b": 3})
    assert response.status_code == 200
    assert response.json == {"result": 2}


def test_multiply_endpoint(client):
    response = client.post("/multiply", json={"a": 4, "b": 6})
    assert response.status_code == 200
    assert response.json == {"result": 24}


def test_divide_endpoint(client):
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json == {"result": 5}


def test_health_check_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"
    assert response.json["service"] == "math_utils_api"
    assert response.json["version"] == "0.1.0"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_not_found_endpoint(client):
    response = client.get("/nonexistent")
    assert response.status_code == 404
    assert response.json == {"error": "Endpoint not found"}


def test_method_not_allowed(client):
    response = client.get("/add")  # GET instead of POST
    assert response.status_code == 405
    assert response.json == {"error": "Method not allowed"}


def test_divide_by_zero_endpoint(client):
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert "error" in response.json
    assert "Cannot divide by zero" in response.json["error"]


def test_missing_json_data(client):
    response = client.post("/add")
    assert response.status_code == 400
    assert response.json == {"error": "No JSON data provided"}


def test_missing_parameters(client):
    response = client.post("/add", json={"a": 5})
    assert response.status_code == 400
    expected_error = "Missing required parameters 'a' and 'b'"
    assert response.json == {"error": expected_error}


def test_invalid_parameter_types(client):
    response = client.post("/multiply", json={"a": "not_a_number", "b": 3})
    assert response.status_code == 400
    expected_error = "Parameters 'a' and 'b' must be numeric"
    assert response.json == {"error": expected_error}


def test_empty_json_data(client):
    response = client.post("/subtract", json={})
    assert response.status_code == 400
    expected_error = "Missing required parameters 'a' and 'b'"
    assert response.json == {"error": expected_error}


def test_null_parameters(client):
    response = client.post("/add", json={"a": None, "b": 5})
    assert response.status_code == 400
    expected_error = "Parameters 'a' and 'b' must be numeric"
    assert response.json == {"error": expected_error}
