import pytest
from datetime import datetime
from pydantic import ValidationError
from src.models.stock import Item, OrderItem, Order, ErrorResponse, OrderStatus

# Test Item model
def test_item_valid():
    item = Item(
        name="Test Item",
        description="A test item",
        price=10.99,
        stock=100,
        sku="TEST123"
    )
    assert item.id is None
    assert item.name == "TEST ITEM"  # Should be uppercase
    assert item.description == "A test item"
    assert item.price == 10.99
    assert item.stock == 100
    assert item.sku == "TEST123"  # Should be uppercase

def test_item_invalid_price():
    with pytest.raises(ValidationError) as exc_info:
        Item(
            name="Test Item",
            description="A test item",
            price=-1.0,
            stock=100,
            sku="TEST123"
        )
    assert "greater than 0" in str(exc_info.value)

def test_item_invalid_name_length():
    with pytest.raises(ValidationError) as exc_info:
        Item(
            name="A",  # Too short
            description="A test item",
            price=10.99,
            stock=100,
            sku="TEST123"
        )
    assert "String should have at least 2 characters" in str(exc_info.value)

# Test OrderItem model
def test_order_item_valid():
    order_item = OrderItem(
        item_id=1,
        quantity=5
    )
    assert order_item.id is None
    assert order_item.item_id == 1
    assert order_item.quantity == 5

def test_order_item_invalid_quantity():
    with pytest.raises(ValidationError) as exc_info:
        OrderItem(
            item_id=1,
            quantity=0
        )
    assert "greater than 0" in str(exc_info.value)

# Test Order model
def test_order_valid():
    order_item = OrderItem(item_id=1, quantity=5)
    order = Order(
        items=[order_item],
        customer_email="test@example.com",
        total_amount=50.99
    )
    assert order.id is None
    assert len(order.items) == 1
    assert order.items[0] == order_item
    assert order.customer_email == "test@example.com"
    assert order.status == OrderStatus.pending
    assert order.total_amount == 50.99
    assert isinstance(order.created_at, datetime)

def test_order_invalid_email():
    order_item = OrderItem(item_id=1, quantity=5)
    with pytest.raises(ValidationError) as exc_info:
        Order(
            items=[order_item],
            customer_email="invalid-email",
            total_amount=50.99
        )
    assert "String should match pattern" in str(exc_info.value)

def test_order_empty_items():
    with pytest.raises(ValidationError) as exc_info:
        Order(
            items=[],
            customer_email="test@example.com",
            total_amount=50.99
        )
    assert "Order must have at least one item" in str(exc_info.value)

# Test ErrorResponse model
def test_error_response_valid():
    error_response = ErrorResponse(
        error="NotFound",
        message="Item not found",
        timestamp=datetime.now(),
        path="/api/items/1"
    )
    assert error_response.error == "NotFound"
    assert error_response.message == "Item not found"
    assert isinstance(error_response.timestamp, datetime)
    assert error_response.path == "/api/items/1"

def test_error_response_no_path():
    error_response = ErrorResponse(
        error="NotFound",
        message="Item not found",
        timestamp=datetime.now()
    )
    assert error_response.path is None
