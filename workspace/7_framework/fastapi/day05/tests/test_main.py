import pytest
from fastapi.testclient import TestClient
from src.main import app, items_db, orders_db

# Create a fixture to reset the in-memory database before each test
@pytest.fixture(autouse=True)
def reset_db():
    global items_db, orders_db, next_item_id, next_order_id
    items_db.clear()
    orders_db.clear()
    next_item_id = 1
    next_order_id = 1
    yield  # Ensure cleanup happens after each test

# Create a FastAPI test client
@pytest.fixture
def client():
    return TestClient(app)

# Test Item endpoints
def test_create_item(client):
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    }
    response = client.post("/items/", json=item_data)
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "TEST ITEM",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    }
    assert len(items_db) == 1

def test_create_item_duplicate_sku(client):
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    }
    client.post("/items/", json=item_data)  # Create first item
    response = client.post("/items/", json=item_data)  # Try to create duplicate
    assert response.status_code == 409
    assert response.json()["error"] == "Duplicate Item"
    assert "already exists" in response.json()["message"]

def test_get_item(client):
    response = client.get("/items/999")  # Non-existent item
    assert response.status_code == 404
    assert response.json()["error"] == "Item Not Found"
    assert "not found" in response.json()["message"]

def test_get_item_found(client):
    item_data = {
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    }
    res = client.post("/items/", json=item_data)
    item_id = res.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id
    assert response.json()["name"] == "TEST ITEM"

def test_get_all_items(client):
    item_data1 = {
        "name": "Item 1",
        "description": "First item",
        "price": 10.99,
        "stock": 100,
        "sku": "SKU1"
    }
    item_data2 = {
        "name": "Item 2",
        "description": "Second item",
        "price": 20.99,
        "stock": 50,
        "sku": "SKU2"
    }
    client.post("/items/", json=item_data1)
    client.post("/items/", json=item_data2)
    response = client.get("/items/")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["sku"] == "SKU1"
    assert response.json()[1]["sku"] == "SKU2"

def test_update_item(client):
    response = client.put("/items/998", json={
        "name": "Updated Item",
        "description": "Updated description",
        "price": 15.99,
        "stock": 200,
        "sku": "NEW123"
    })
    assert response.status_code == 404
    assert response.json()["error"] == "Item Not Found"

def test_update_item_found(client):
    resp = client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    })
    item_id = resp.json()["id"]
    update_data = {
        "name": "Updated Item",
        "description": "Updated description",
        "price": 15.99,
        "stock": 200,
        "sku": "NEW123"
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    assert response.json() == {
        "id": item_id,
        "name": "UPDATED ITEM",
        "description": "Updated description",
        "price": 15.99,
        "stock": 200,
        "sku": "NEW123"
    }

def test_delete_item(client):
    response = client.delete("/items/999")
    assert response.status_code == 404
    assert response.json()["error"] == "Item Not Found"

def test_delete_item_found(client):
    resp = client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    })
    item_id = resp.json()["id"]
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 204
    assert len(items_db) == 0

# Test Order endpoints
def test_create_order(client):
    resp =client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    })
    order_data = {
        "items": [{"item_id": resp.json()["id"], "quantity": 5}],
        "customer_email": "test@example.com",
        "total_amount": 54.95
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 201
    assert response.json()["id"] == response.json()["id"]
    assert response.json()["status"] == "pending"
    assert response.json()["total_amount"] == 54.95
    assert len(orders_db) == 1
    assert items_db[0]["stock"] == 95  # Stock reduced by 5

def test_create_order_insufficient_stock(client):
    resp = client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 2,
        "sku": "TEST123"
    })
    order_data = {
        "items": [{"item_id": resp.json()["id"], "quantity": 5}],
        "customer_email": "test@example.com",
        "total_amount": 54.95
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 409
    assert response.json()["error"] == "Insufficient Stock"
    assert "Insufficient stock" in response.json()["message"]

def test_get_order(client):
    response = client.get("/orders/999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]

def test_get_order_found(client):
    resp = client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    })
    resp_order = client.post("/orders/", json={
        "items": [{"item_id": resp.json()["id"], "quantity": 5}],
        "customer_email": "test@example.com",
        "total_amount": 54.95
    })
    order_id = resp_order.json()["id"]
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == response.json()["id"]
    assert response.json()["status"] == "pending"

def test_update_order_status(client):
    resp = client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    })
    resp_order = client.post("/orders/", json={
        "items": [{"item_id": resp.json()["id"], "quantity": 5}],
        "customer_email": "test@example.com",
        "total_amount": 54.95
    })

    response = client.patch(f"/orders/{resp_order.json()['id']}/status?new_status=processing")
    assert response.status_code == 200
    assert response.json()["status"] == "processing"

def test_update_order_status_invalid_transition(client):
    resp =client.post("/items/", json={
        "name": "Test Item",
        "description": "A test item",
        "price": 10.99,
        "stock": 100,
        "sku": "TEST123"
    })
    resp_order = client.post("/orders/", json={
        "items": [{"item_id": resp.json()["id"], "quantity": 5}],
        "customer_email": "test@example.com",
        "total_amount": 54.95
    })

    response = client.patch(f"/orders/{resp_order.json()['id']}/status?new_status=delivered")
    assert response.status_code == 400
    assert "Cannot transition" in response.json()["detail"]

# Test Health endpoint
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert "timestamp" in response.json()
    assert response.json()["items_count"] == 0
    assert response.json()["orders_count"] == 0
