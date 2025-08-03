import pytest
import time
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from pydantic import ValidationError

# Import the main application and related components
from src.main import app, db, ItemDatabase, AppConfig, get_request_info
from src.main import ItemCreate, ItemResponse, HealthResponse


class TestItemDatabase:
    """Test cases for ItemDatabase class."""

    @pytest.fixture
    def item_db(self):
        """Create a fresh ItemDatabase instance."""
        return ItemDatabase()

    def test_initial_data(self, item_db):
        """Test that database starts with initial data."""
        items = item_db.get_all()
        assert len(items) == 3
        assert all(item["id"] in [1, 2, 3] for item in items)

    def test_get_all_returns_copy(self, item_db):
        """Test that get_all returns a copy, not reference."""
        items1 = item_db.get_all()
        items2 = item_db.get_all()

        # Should be equal but not the same object
        assert items1 == items2
        assert items1 is not items2

    def test_get_by_id_existing(self, item_db):
        """Test getting an existing item by ID."""
        item = item_db.get_by_id(1)
        assert item is not None
        assert item["id"] == 1
        assert item["name"] == "Item 1"

    def test_get_by_id_non_existing(self, item_db):
        """Test getting a non-existing item by ID."""
        item = item_db.get_by_id(999)
        assert item is None

    def test_create_item(self, item_db):
        """Test creating a new item."""
        item_data = ItemCreate(name="New Item", price=25.0, description="New description")
        new_item = item_db.create(item_data)

        assert new_item["id"] == 4  # Next available ID
        assert new_item["name"] == "New Item"
        assert new_item["price"] == 25.0
        assert new_item["description"] == "New description"
        assert "created_at" in new_item

        # Verify it's in the database
        assert len(item_db.get_all()) == 4

    def test_update_existing_item(self, item_db):
        """Test updating an existing item."""
        item_data = ItemCreate(name="Updated Item", price=30.0, description="Updated description")
        updated_item = item_db.update(1, item_data)

        assert updated_item is not None
        assert updated_item["id"] == 1
        assert updated_item["name"] == "Updated Item"
        assert updated_item["price"] == 30.0
        assert updated_item["description"] == "Updated description"

    def test_update_non_existing_item(self, item_db):
        """Test updating a non-existing item."""
        item_data = ItemCreate(name="Updated Item", price=30.0)
        updated_item = item_db.update(999, item_data)

        assert updated_item is None

    def test_delete_existing_item(self, item_db):
        """Test deleting an existing item."""
        result = item_db.delete(1)
        assert result is True

        # Verify it's gone
        assert item_db.get_by_id(1) is None
        assert len(item_db.get_all()) == 2

    def test_delete_non_existing_item(self, item_db):
        """Test deleting a non-existing item."""
        result = item_db.delete(999)
        assert result is False


class TestPydanticModels:
    """Test cases for Pydantic models."""

    def test_item_create_valid(self):
        """Test ItemCreate with valid data."""
        item = ItemCreate(name="Test Item", price=10.0, description="Test description")
        assert item.name == "Test Item"
        assert item.price == 10.0
        assert item.description == "Test description"

    def test_item_create_invalid_name(self):
        """Test ItemCreate with invalid name."""
        with pytest.raises(ValidationError):
            ItemCreate(name="", price=10.0)  # Empty name

    def test_item_create_invalid_price(self):
        """Test ItemCreate with invalid price."""
        with pytest.raises(ValidationError):
            ItemCreate(name="Test", price=-10.0)  # Negative price

        with pytest.raises(ValidationError):
            ItemCreate(name="Test", price=0)  # Zero price

    def test_item_response_model(self):
        """Test ItemResponse model."""
        item_data = {
            "id": 1,
            "name": "Test Item",
            "price": 10.0,
            "created_at": time.time(),
            "description": "Test description"
        }
        item = ItemResponse(**item_data)
        assert item.id == 1
        assert item.name == "Test Item"

    def test_health_response_model(self):
        """Test HealthResponse model."""
        health = HealthResponse(
            status="healthy",
            timestamp=time.time(),
            version="2.0.0"
        )
        assert health.status == "healthy"
        assert health.middleware_active is True  # Default value


class TestAppConfig:
    """Test cases for AppConfig class."""

    def test_default_config(self):
        """Test default configuration values."""
        with patch.dict('os.environ', {}, clear=True):
            config = AppConfig()
            assert config.environment == "development"
            assert config.debug is True
            assert config.max_request_size == 2 * 1024 * 1024
            assert config.rate_limit_calls == 50
            assert config.rate_limit_period == 60

    def test_production_config(self):
        """Test production configuration."""
        with patch.dict('os.environ', {'ENVIRONMENT': 'production'}):
            config = AppConfig()
            assert config.environment == "production"
            assert config.debug is False

    def test_custom_environment_variables(self):
        """Test custom environment variables."""
        env_vars = {
            'ENVIRONMENT': 'staging',
            'MAX_REQUEST_SIZE': '5242880',  # 5MB
            'RATE_LIMIT_CALLS': '100',
            'RATE_LIMIT_PERIOD': '300'
        }
        with patch.dict('os.environ', env_vars):
            config = AppConfig()
            assert config.environment == "staging"
            assert config.max_request_size == 5242880
            assert config.rate_limit_calls == 100
            assert config.rate_limit_period == 300


class TestAPIEndpoints:
    """Test cases for API endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    @pytest.fixture
    def reset_database(self):
        """Reset database to initial state before each test."""
        # Store original items
        original_items = db.items.copy()
        original_next_id = db._next_id

        yield

        # Restore original state
        db.items = original_items
        db._next_id = original_next_id

    def test_root_endpoint(self, client):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Welcome to Enhanced Middleware Demo API"
        assert data["version"] == "2.0.0"
        assert "request_id" in data
        assert "timestamp" in data

    def test_get_items(self, client, reset_database):
        """Test getting all items."""
        response = client.get("/items/")
        assert response.status_code == 200

        data = response.json()
        assert "items" in data
        assert "count" in data
        assert data["count"] == 3
        assert len(data["items"]) == 3

    def test_get_item_existing(self, client, reset_database):
        """Test getting an existing item."""
        response = client.get("/items/1")
        assert response.status_code == 200

        data = response.json()
        assert "item" in data
        assert data["item"]["id"] == 1
        assert data["item"]["name"] == "Item 1"

    def test_get_item_not_found(self, client, reset_database):
        """Test getting a non-existing item."""
        response = client.get("/items/999")
        assert response.status_code == 404

        data = response.json()
        # The custom exception handler returns 'error' field, not 'detail'
        assert "Item with ID 999 not found" in data["error"]

    def test_create_item(self, client, reset_database):
        """Test creating a new item."""
        item_data = {
            "name": "New Test Item",
            "price": 25.5,
            "description": "A test item"
        }
        response = client.post("/items/", json=item_data)
        assert response.status_code == 201

        data = response.json()
        assert "item" in data
        assert data["item"]["name"] == "New Test Item"
        assert data["item"]["price"] == 25.5
        assert data["message"] == "Item created successfully"

    def test_create_item_invalid_data(self, client):
        """Test creating item with invalid data."""
        invalid_data = {
            "name": "",  # Invalid: empty name
            "price": -10  # Invalid: negative price
        }
        response = client.post("/items/", json=invalid_data)
        assert response.status_code == 422  # Validation error

    def test_update_item(self, client, reset_database):
        """Test updating an existing item."""
        update_data = {
            "name": "Updated Item",
            "price": 35.0,
            "description": "Updated description"
        }
        response = client.put("/items/1", json=update_data)
        assert response.status_code == 200

        data = response.json()
        assert data["item"]["name"] == "Updated Item"
        assert data["item"]["price"] == 35.0
        assert data["message"] == "Item updated successfully"

    def test_update_item_not_found(self, client, reset_database):
        """Test updating a non-existing item."""
        update_data = {
            "name": "Updated Item",
            "price": 35.0
        }
        response = client.put("/items/999", json=update_data)
        assert response.status_code == 404

    def test_delete_item(self, client, reset_database):
        """Test deleting an existing item."""
        response = client.delete("/items/1")
        assert response.status_code == 200

        # Verify item was deleted
        verify_response = client.get("/items/1")
        assert verify_response.status_code == 404

    def test_delete_item_not_found(self, client, reset_database):
        """Test deleting a non-existing item."""
        response = client.delete("/items/999")
        assert response.status_code == 404

    def test_large_data_endpoint(self, client):
        """Test large data endpoint."""
        response = client.get("/large-data?size=100")
        assert response.status_code == 200

        data = response.json()
        assert len(data["data"]) == 100
        assert data["metadata"]["count"] == 100

    def test_large_data_size_limit(self, client):
        """Test large data endpoint with size too large."""
        response = client.get("/large-data?size=20000")
        assert response.status_code == 400

    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert data["middleware_active"] is True
        assert data["version"] == "2.0.0"

    def test_metrics_endpoint(self, client):
        """Test metrics endpoint."""
        response = client.get("/metrics")
        assert response.status_code == 200

        data = response.json()
        assert "items_count" in data
        assert "environment" in data
        assert "uptime_check" in data

    def test_error_test_endpoint(self, client):
        """Test error endpoint triggers error handling."""
        response = client.get("/error-test")
        assert response.status_code == 500

        data = response.json()
        assert data["error"] == "Internal Server Error"
        assert "request_id" in data

    def test_slow_endpoint(self, client):
        """Test slow endpoint."""
        response = client.get("/slow-endpoint?delay=0.1")
        assert response.status_code == 200

        data = response.json()
        assert "Processed after" in data["message"]

    def test_slow_endpoint_delay_limit(self, client):
        """Test slow endpoint with delay too long."""
        response = client.get("/slow-endpoint?delay=15")
        assert response.status_code == 400

    def test_rate_limit_test_endpoint(self, client):
        """Test rate limit test endpoint."""
        response = client.get("/rate-limit-test")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Rate limit test successful"
        assert "info" in data

    def test_cors_preflight_endpoint(self, client):
        """Test CORS preflight endpoint."""
        response = client.options("/cors-preflight")
        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "CORS preflight successful"


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_get_request_info(self):
        """Test get_request_info function."""
        mock_request = Mock()
        mock_request.state = Mock()
        mock_request.state.request_id = "test-request-id"
        mock_request.state.correlation_id = "test-correlation-id"

        with patch('time.time', return_value=1234567890.0):
            info = get_request_info(mock_request)

        assert info["request_id"] == "test-request-id"
        assert info["correlation_id"] == "test-correlation-id"
        assert info["timestamp"] == 1234567890.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
