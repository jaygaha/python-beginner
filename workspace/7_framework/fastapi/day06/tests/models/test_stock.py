import unittest
from datetime import datetime
from pydantic import ValidationError
from src.enums.order_enum import OrderStatus
from src.models.stock import Item, OrderItem, Order, ErrorResponse

class TestPydanticModels(unittest.TestCase):

    def test_valid_item(self):
        """Test creating a valid Item object."""
        item = Item(id=1, name="Laptop", price=999.99, owner_id=100, is_active=True)
        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, "Laptop")
        self.assertEqual(item.price, 999.99)
        self.assertEqual(item.owner_id, 100)
        self.assertTrue(item.is_active)

    def test_invalid_item_negative_price(self):
        """Test Item with negative price raises ValidationError."""
        with self.assertRaises(ValidationError):
            Item(name="Phone", price=-10, owner_id=100)

    def test_invalid_item_short_name(self):
        """Test Item with too-short name raises ValidationError."""
        with self.assertRaises(ValidationError):
            Item(name="A", price=50, owner_id=100)

    def test_valid_order_item(self):
        """Test creating a valid OrderItem object."""
        order_item = OrderItem(id=1, item_id=10, quantity=2)
        self.assertEqual(order_item.id, 1)
        self.assertEqual(order_item.item_id, 10)
        self.assertEqual(order_item.quantity, 2)

    def test_invalid_order_item_zero_quantity(self):
        """Test OrderItem with zero quantity raises ValidationError."""
        with self.assertRaises(ValidationError):
            OrderItem(item_id=10, quantity=0)

    def test_valid_order(self):
        """Test creating a valid Order object."""
        order_item = OrderItem(item_id=1, quantity=1)
        order = Order(
            id=1,
            items=[order_item],
            customer_email="test@example.com",
            status=OrderStatus.pending,
            total_amount=100.0
        )
        self.assertEqual(order.id, 1)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.customer_email, "test@example.com")
        self.assertEqual(order.status, OrderStatus.pending)
        self.assertEqual(order.total_amount, 100.0)
        self.assertIsInstance(order.created_at, datetime)

    def test_order_default_values(self):
        """Test Order with default status and created_at."""
        order_item = OrderItem(item_id=1, quantity=1)
        order = Order(items=[order_item], customer_email="test@example.com", total_amount=100.0)
        self.assertEqual(order.status, OrderStatus.pending)
        self.assertIsInstance(order.created_at, datetime)

    def test_invalid_order_empty_items(self):
        """Test Order with empty items list raises ValidationError."""
        with self.assertRaises(ValidationError):
            Order(items=[], customer_email="test@example.com", total_amount=100.0)

    def test_invalid_order_invalid_email(self):
        """Test Order with invalid email raises ValidationError."""
        order_item = OrderItem(item_id=1, quantity=1)
        with self.assertRaises(ValidationError):
            Order(items=[order_item], customer_email="invalid-email", total_amount=100.0)

    def test_invalid_order_negative_total(self):
        """Test Order with negative total_amount raises ValidationError."""
        order_item = OrderItem(item_id=1, quantity=1)
        with self.assertRaises(ValidationError):
            Order(items=[order_item], customer_email="test@example.com", total_amount=-10.0)

    def test_valid_error_response(self):
        """Test creating a valid ErrorResponse object."""
        error_response = ErrorResponse(
            error="NotFound",
            message="Resource not found",
            timestamp=datetime(2025, 8, 3),
            path="/api/resource"
        )
        self.assertEqual(error_response.error, "NotFound")
        self.assertEqual(error_response.message, "Resource not found")
        self.assertEqual(error_response.timestamp, datetime(2025, 8, 3))
        self.assertEqual(error_response.path, "/api/resource")

    def test_error_response_optional_path(self):
        """Test ErrorResponse with optional path set to None."""
        error_response = ErrorResponse(
            error="ValidationError",
            message="Invalid input",
            timestamp=datetime(2025, 8, 3)
        )
        self.assertIsNone(error_response.path)

if __name__ == '__main__':
    unittest.main()
