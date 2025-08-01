from fastapi.testclient import TestClient
from src.main import app
import io

client = TestClient(app)

def test_create_product():
    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 29.99,
        "category": "electronics",
        "tags": ["test", "product"]
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 29.99
    assert "id" in data

def test_update_product():
    # Create product first
    product_data = {
        "name": "Update Test",
        "price": 19.99,
        "category": "books"
    }
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    # Update product
    update_data = {"name": "Updated Product", "price": 24.99}
    response = client.put(f"/products/{product_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

def test_create_products_batch():
    products_data = [
        {"name": "Product 1", "price": 10.0, "category": "cat1"},
        {"name": "Product 2", "price": 20.0, "category": "cat2"}
    ]
    response = client.post("/products/batch/", json=products_data)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Product 1"

def test_update_user_profile():
    profile_data = {
        "bio": "Software developer",
        "website": "https://example.com",
        "location": "New York"
    }
    response = client.post("/users/1/profile", json=profile_data)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["profile"]["bio"] == "Software developer"

def test_submit_contact_form():
    contact_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Test Subject",
        "message": "This is a test message",
        "urgent": False
    }
    response = client.post("/contact/", json=contact_data)
    assert response.status_code == 200
    data = response.json()
    assert "reference_id" in data

def test_create_product_form():
    form_data = {
        "name": "Form Product",
        "description": "Created via form",
        "price": 15.99,
        "category": "tools",
        "tags": "form, test, product"
    }
    response = client.post("/products/form/", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Form Product"
    assert "form" in data["tags"]

def test_upload_file():
    file_content = b"test file content"
    files = {"file": ("test.txt", io.BytesIO(file_content), "text/plain")}
    response = client.post("/upload/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["filename"] == "test.txt"
    assert data["content_type"] == "text/plain"

def test_upload_multiple_files():
    files = [
        ("files", ("test1.txt", io.BytesIO(b"content1"), "text/plain")),
        ("files", ("test2.txt", io.BytesIO(b"content2"), "text/plain"))
    ]
    response = client.post("/upload/multiple/", files=files)
    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2

def test_add_product_review():
    # Create product first
    product_data = {"name": "Review Test", "price": 9.99, "category": "test"}
    create_response = client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    # Add review
    form_data = {
        "rating": 5,
        "title": "Great product!",
        "content": "I really liked this product",
        "anonymous": False
    }
    response = client.post(f"/products/{product_id}/review/", data=form_data)
    assert response.status_code == 200
    data = response.json()
    assert data["rating"] == 5
    assert data["title"] == "Great product!"
