import json
import unittest
import tornado.ioloop
import tornado.testing
import tornado.web
import app
from app import make_app

class TestRestApi(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        """Return the app instance for testing"""
        return make_app()

    def setUp(self):
        """Set up test fixtures before each test method"""
        super().setUp()
        # Reset items to initial state before each test
        app.items.clear()
        app.items.extend([
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ])

    def test_get_items_success(self):
        """Test GET /items returns all items"""
        response = self.fetch("/items")

        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        data = json.loads(response.body)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["name"], "Item 1")
        self.assertEqual(data[1]["name"], "Item 2")
        self.assertEqual(data[2]["name"], "Item 3")

    def test_get_items_empty_list(self):
        """Test GET /items returns empty list when no items exist"""
        # Clear all items
        app.items.clear()

        response = self.fetch("/items")

        self.assertEqual(response.code, 200)
        data = json.loads(response.body)
        self.assertEqual(data, [])

    def test_post_item_success(self):
        """Test POST /items creates a new item successfully"""
        body = json.dumps({"name": "New Test Item"})
        response = self.fetch(
            "/items",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(response.code, 201)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        data = json.loads(response.body)
        self.assertIn("id", data)
        self.assertEqual(data["name"], "New Test Item")
        self.assertEqual(data["id"], 4)  # Should be next available ID

        # Verify item was added to the list
        self.assertEqual(len(app.items), 4)
        self.assertEqual(app.items[-1]["name"], "New Test Item")

    def test_post_item_empty_list(self):
        """Test POST /items creates item with ID 1 when list is empty"""
        app.items.clear()

        body = json.dumps({"name": "First Item"})
        response = self.fetch(
            "/items",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(response.code, 201)
        data = json.loads(response.body)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "First Item")

    def test_post_item_invalid_json(self):
        """Test POST /items with invalid JSON returns 400"""
        response = self.fetch(
            "/items",
            method="POST",
            body="invalid json",
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(response.code, 400)
        data = json.loads(response.body)
        self.assertIn("error", data)

    def test_post_item_missing_name(self):
        """Test POST /items with missing name field returns 400"""
        body = json.dumps({"description": "Missing name field"})
        response = self.fetch(
            "/items",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(response.code, 400)
        data = json.loads(response.body)
        self.assertIn("error", data)

    def test_get_item_success(self):
        """Test GET /items/{id} returns specific item"""
        response = self.fetch("/items/1")

        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        data = json.loads(response.body)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Item 1")

    def test_get_item_not_found(self):
        """Test GET /items/{id} returns 404 for non-existent item"""
        response = self.fetch("/items/999")

        self.assertEqual(response.code, 404)
        data = json.loads(response.body)
        self.assertEqual(data["error"], "Item not found")

    def test_get_item_invalid_id(self):
        """Test GET /items/{id} with invalid ID format"""
        response = self.fetch("/items/abc")

        # Should return 404 as the route pattern only matches numbers
        self.assertEqual(response.code, 404)

    def test_put_item_success(self):
        """Test PUT /items/{id} updates existing item"""
        body = json.dumps({"name": "Updated Item 1"})
        response = self.fetch(
            "/items/1",
            method="PUT",
            body=body,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        data = json.loads(response.body)
        self.assertEqual(data["id"], 1)
        self.assertEqual(data["name"], "Updated Item 1")

        # Verify the item was actually updated in the list
        updated_item = next(item for item in app.items if item["id"] == 1)
        self.assertEqual(updated_item["name"], "Updated Item 1")

    def test_put_item_not_found(self):
        """Test PUT /items/{id} returns 404 for non-existent item"""
        body = json.dumps({"name": "Updated Item"})
        response = self.fetch(
            "/items/999",
            method="PUT",
            body=body,
            headers={"Content-Type": "application/json"}
        )

        self.assertEqual(response.code, 404)
        data = json.loads(response.body)
        self.assertEqual(data["error"], "Item not found")

    def test_put_item_invalid_json(self):
        """Test PUT /items/{id} with invalid JSON"""
        response = self.fetch(
            "/items/1",
            method="PUT",
            body="invalid json",
            headers={"Content-Type": "application/json"}
        )

        # The PUT endpoint now handles JSON parsing errors properly
        self.assertEqual(response.code, 400)
        data = json.loads(response.body)
        self.assertIn("error", data)

    def test_delete_item_success(self):
        """Test DELETE /items/{id} removes item successfully"""
        # Verify item exists before deletion
        self.assertEqual(len(app.items), 3)
        self.assertTrue(any(item["id"] == 2 for item in app.items))

        response = self.fetch("/items/2", method="DELETE")

        self.assertEqual(response.code, 204)
        self.assertEqual(response.body, b"")

        # Verify item was removed from the list
        self.assertEqual(len(app.items), 2)
        self.assertFalse(any(item["id"] == 2 for item in app.items))

    def test_delete_item_not_found(self):
        """Test DELETE /items/{id} for non-existent item still returns 204"""
        initial_count = len(app.items)

        response = self.fetch("/items/999", method="DELETE")

        self.assertEqual(response.code, 204)
        # List should remain unchanged
        self.assertEqual(len(app.items), initial_count)

    def test_delete_all_items(self):
        """Test deleting all items one by one"""
        # Delete all items
        for item_id in [1, 2, 3]:
            response = self.fetch(f"/items/{item_id}", method="DELETE")
            self.assertEqual(response.code, 204)

        # Verify all items are gone
        self.assertEqual(len(app.items), 0)

        # Verify GET returns empty list
        response = self.fetch("/items")
        self.assertEqual(response.code, 200)
        data = json.loads(response.body)
        self.assertEqual(data, [])

    def test_content_type_headers(self):
        """Test that all endpoints return correct Content-Type headers"""
        # Test GET /items
        response = self.fetch("/items")
        self.assertEqual(response.headers["Content-Type"], "application/json")

        # Test GET /items/{id}
        response = self.fetch("/items/1")
        self.assertEqual(response.headers["Content-Type"], "application/json")

        # Test POST /items
        body = json.dumps({"name": "Test Item"})
        response = self.fetch(
            "/items",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")

        # Test PUT /items/{id}
        body = json.dumps({"name": "Updated Item"})
        response = self.fetch(
            "/items/1",
            method="PUT",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.headers["Content-Type"], "application/json")

    def test_invalid_endpoints(self):
        """Test requests to invalid endpoints return 404"""
        # Test non-existent endpoint
        response = self.fetch("/invalid")
        self.assertEqual(response.code, 404)

        # Test invalid method on valid endpoint
        response = self.fetch("/items", method="PATCH", body="", allow_nonstandard_methods=True)
        self.assertEqual(response.code, 405)  # Method Not Allowed

    def test_integration_workflow(self):
        """Test complete CRUD workflow integration"""
        # 1. Get initial items
        response = self.fetch("/items")
        self.assertEqual(response.code, 200)
        initial_items = json.loads(response.body)
        initial_count = len(initial_items)

        # 2. Create new item
        body = json.dumps({"name": "Integration Test Item"})
        response = self.fetch(
            "/items",
            method="POST",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.code, 201)
        new_item = json.loads(response.body)
        new_id = new_item["id"]

        # 3. Verify item was created
        response = self.fetch(f"/items/{new_id}")
        self.assertEqual(response.code, 200)
        retrieved_item = json.loads(response.body)
        self.assertEqual(retrieved_item["name"], "Integration Test Item")

        # 4. Update the item
        body = json.dumps({"name": "Updated Integration Test Item"})
        response = self.fetch(
            f"/items/{new_id}",
            method="PUT",
            body=body,
            headers={"Content-Type": "application/json"}
        )
        self.assertEqual(response.code, 200)
        updated_item = json.loads(response.body)
        self.assertEqual(updated_item["name"], "Updated Integration Test Item")

        # 5. Verify update
        response = self.fetch(f"/items/{new_id}")
        self.assertEqual(response.code, 200)
        retrieved_item = json.loads(response.body)
        self.assertEqual(retrieved_item["name"], "Updated Integration Test Item")

        # 6. Delete the item
        response = self.fetch(f"/items/{new_id}", method="DELETE")
        self.assertEqual(response.code, 204)

        # 7. Verify deletion
        response = self.fetch(f"/items/{new_id}")
        self.assertEqual(response.code, 404)

        # 8. Verify final count
        response = self.fetch("/items")
        self.assertEqual(response.code, 200)
        final_items = json.loads(response.body)
        self.assertEqual(len(final_items), initial_count)


if __name__ == "__main__":
    # Run the tests
    unittest.main()
