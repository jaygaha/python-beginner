import pytest
from src.enums.order_enum import OrderStatus

def test_order_status_values():
    """Test that all enum values match their string representations."""
    assert OrderStatus.pending.value == "pending"
    assert OrderStatus.processing.value == "processing"
    assert OrderStatus.shipped.value == "shipped"
    assert OrderStatus.delivered.value == "delivered"
    assert OrderStatus.cancelled.value == "cancelled"

def test_order_status_names():
    """Test that enum names match expected values."""
    assert OrderStatus.pending.name == "pending"
    assert OrderStatus.processing.name == "processing"
    assert OrderStatus.shipped.name == "shipped"
    assert OrderStatus.delivered.name == "delivered"
    assert OrderStatus.cancelled.name == "cancelled"

def test_order_status_members():
    """Test that all expected members are present in the enum."""
    expected_members = {"pending", "processing", "shipped", "delivered", "cancelled"}
    actual_members = {member.name for member in OrderStatus}
    assert actual_members == expected_members

def test_order_status_is_string():
    """Test that enum values are strings."""
    for member in OrderStatus:
        assert isinstance(member.value, str)

def test_order_status_from_string():
    """Test that enum can be accessed by string value."""
    assert OrderStatus("pending") == OrderStatus.pending
    assert OrderStatus("processing") == OrderStatus.processing
    assert OrderStatus("shipped") == OrderStatus.shipped
    assert OrderStatus("delivered") == OrderStatus.delivered
    assert OrderStatus("cancelled") == OrderStatus.cancelled

def test_order_status_invalid_value():
    """Test that invalid string values raise ValueError."""
    with pytest.raises(ValueError):
        OrderStatus("invalid_status")
