import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.api import app


class TestMathUtilsAPI:
    """Test suite for Math Utils API endpoints."""

    @pytest.fixture(scope="class")
    def client(self):
        """Create a test client for the FastAPI application."""
        return TestClient(app)

    @pytest.fixture(scope="class")
    def valid_request_data(self):
        """Provide valid test data for API requests."""
        return {
            "add": {"a": 5, "b": 3},
            "subtract": {"a": 10, "b": 4},
            "multiply": {"a": 6, "b": 7},
            "divide": {"a": 15, "b": 3},
        }

    # Addition endpoint tests
    def test_add_endpoint_success(self, client, valid_request_data):
        """Test successful addition operation."""
        response = client.post("/add", json=valid_request_data["add"])

        assert response.status_code == status.HTTP_200_OK
        assert response.headers["content-type"] == "application/json"
        response_data = response.json()
        assert "result" in response_data
        assert response_data["result"] == 8

    @pytest.mark.parametrize(
        "a,b,expected",
        [
            (2, 3, 5),
            (-1, 1, 0),
            (0, 0, 0),
            (-5, -3, -8),
            (2.5, 1.5, 4.0),
            (100, -50, 50),
        ],
    )
    def test_add_endpoint_various_inputs(self, client, a, b, expected):
        """Test addition with various numeric inputs."""
        response = client.post("/add", json={"a": a, "b": b})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result == pytest.approx(expected, rel=1e-9)

    # Subtraction endpoint tests
    def test_subtract_endpoint_success(self, client, valid_request_data):
        """Test successful subtraction operation."""
        response = client.post("/subtract", json=valid_request_data["subtract"])

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "result" in response_data
        assert response_data["result"] == 6

    @pytest.mark.parametrize(
        "a,b,expected",
        [(10, 3, 7), (5, 10, -5), (0, 5, -5), (-3, -8, 5), (2.7, 1.2, 1.5)],
    )
    def test_subtract_endpoint_various_inputs(self, client, a, b, expected):
        """Test subtraction with various numeric inputs."""
        response = client.post("/subtract", json={"a": a, "b": b})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result == pytest.approx(expected, rel=1e-9)

    # Multiplication endpoint tests
    def test_multiply_endpoint_success(self, client, valid_request_data):
        """Test successful multiplication operation."""
        response = client.post("/multiply", json=valid_request_data["multiply"])

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "result" in response_data
        assert response_data["result"] == 42

    @pytest.mark.parametrize(
        "a,b,expected",
        [(4, 5, 20), (-3, 4, -12), (0, 100, 0), (-2, -6, 12), (2.5, 4, 10.0)],
    )
    def test_multiply_endpoint_various_inputs(self, client, a, b, expected):
        """Test multiplication with various numeric inputs."""
        response = client.post("/multiply", json={"a": a, "b": b})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result == pytest.approx(expected, rel=1e-9)

    # Division endpoint tests
    def test_divide_endpoint_success(self, client, valid_request_data):
        """Test successful division operation."""
        response = client.post("/divide", json=valid_request_data["divide"])

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert "result" in response_data
        assert response_data["result"] == 5.0

    @pytest.mark.parametrize(
        "a,b,expected",
        [(10, 2, 5.0), (7, 2, 3.5), (-12, 3, -4.0), (15, -3, -5.0), (0, 5, 0.0)],
    )
    def test_divide_endpoint_various_inputs(self, client, a, b, expected):
        """Test division with various numeric inputs."""
        response = client.post("/divide", json={"a": a, "b": b})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result == pytest.approx(expected, rel=1e-9)

    def test_divide_by_zero_error(self, client):
        """Test division by zero returns proper error."""
        response = client.post("/divide", json={"a": 10, "b": 0})

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        response_data = response.json()
        assert "detail" in response_data
        assert response_data["detail"] == "Cannot divide by zero"

    # Input validation tests
    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_invalid_string_input(self, client, endpoint):
        """Test that string inputs return validation error."""
        response = client.post(endpoint, json={"a": "invalid", "b": 3})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_field_a(self, client, endpoint):
        """Test that missing field 'a' returns validation error."""
        response = client.post(endpoint, json={"b": 3})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_missing_field_b(self, client, endpoint):
        """Test that missing field 'b' returns validation error."""
        response = client.post(endpoint, json={"a": 5})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_empty_request_body(self, client, endpoint):
        """Test that empty request body returns validation error."""
        response = client.post(endpoint, json={})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_null_values(self, client, endpoint):
        """Test that null values return validation error."""
        response = client.post(endpoint, json={"a": None, "b": 3})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # HTTP method tests
    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_get_method_not_allowed(self, client, endpoint):
        """Test that GET method is not allowed on calculation endpoints."""
        response = client.get(endpoint)

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_put_method_not_allowed(self, client, endpoint):
        """Test that PUT method is not allowed on calculation endpoints."""
        response = client.put(endpoint, json={"a": 1, "b": 2})

        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED

    # Content type tests
    @pytest.mark.parametrize("endpoint", ["/add", "/subtract", "/multiply", "/divide"])
    def test_invalid_content_type(self, client, endpoint):
        """Test that invalid content type is handled properly."""
        response = client.post(
            endpoint,
            data="a=1&b=2",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    # Edge cases for numeric limits
    def test_large_numbers(self, client):
        """Test calculations with very large numbers."""
        large_num = 1e10
        response = client.post("/add", json={"a": large_num, "b": large_num})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result == pytest.approx(2 * large_num, rel=1e-9)

    def test_very_small_numbers(self, client):
        """Test calculations with very small numbers."""
        small_num = 1e-10
        response = client.post("/multiply", json={"a": small_num, "b": 2})

        assert response.status_code == status.HTTP_200_OK
        result = response.json()["result"]
        assert result == pytest.approx(2 * small_num, rel=1e-9)

    def test_infinity_input(self, client):
        """Test that infinity values are rejected with validation error."""
        response = client.post("/add", json={"a": "inf", "b": 1})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    def test_nan_input(self, client):
        """Test that NaN values are rejected with validation error."""
        response = client.post("/multiply", json={"a": "nan", "b": 5})

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        response_data = response.json()
        assert "detail" in response_data

    # Response format validation
    def test_response_structure_add(self, client):
        """Test that response has correct structure for add endpoint."""
        response = client.post("/add", json={"a": 1, "b": 2})

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()

        # Check response structure
        assert isinstance(response_data, dict)
        assert len(response_data) == 1
        assert "result" in response_data
        assert isinstance(response_data["result"], (int, float))

    def test_overflow_protection(self, client):
        """Test that operations resulting in overflow are handled."""
        # Test with numbers that might cause overflow
        very_large = 1e308
        response = client.post("/multiply", json={"a": very_large, "b": 10})

        # Should either succeed with finite result or return error
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]

    def test_concurrent_requests(self, client):
        """Test that the API can handle multiple concurrent requests."""
        import concurrent.futures

        def make_request():
            return client.post("/add", json={"a": 1, "b": 1})

        # Make multiple concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            responses = [future.result() for future in futures]

        # All requests should succeed
        for response in responses:
            assert response.status_code == status.HTTP_200_OK
            assert response.json()["result"] == 2
