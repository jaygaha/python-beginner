#!/usr/bin/env python3
"""
Test script for Tornado Examples

This script tests the various endpoints and handlers in the examples.py file
to ensure they work correctly. It uses Tornado's AsyncHTTPTestCase for
comprehensive testing.
"""

import json
import unittest
import tornado.testing
import tornado.web
from examples import make_app


class TestTornadoExamples(tornado.testing.AsyncHTTPTestCase):
    """Test suite for Tornado examples."""

    def get_app(self):
        """Return the application instance for testing."""
        return make_app()

    def test_home_page(self):
        """Test the home page loads correctly."""
        response = self.fetch("/")
        self.assertEqual(response.code, 200)
        self.assertIn(b"Welcome to Tornado Examples", response.body)
        self.assertIn(b"<title>Tornado Examples</title>", response.body)

    def test_json_endpoint(self):
        """Test JSON response endpoint."""
        response = self.fetch("/json")
        self.assertEqual(response.code, 200)
        self.assertEqual(response.headers["Content-Type"], "application/json")

        data = json.loads(response.body)
        self.assertIn("message", data)
        self.assertIn("timestamp", data)
        self.assertEqual(data["message"], "Hello from Tornado!")

    def test_form_get(self):
        """Test form display (GET request)."""
        response = self.fetch("/form")
        self.assertEqual(response.code, 200)
        self.assertIn(b"Contact Form", response.body)
        self.assertIn(b'<form method="post"', response.body)
        self.assertIn(b'name="name"', response.body)
        self.assertIn(b'name="email"', response.body)

    def test_form_post_success(self):
        """Test successful form submission."""
        form_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "message": "Test message"
        }

        body = "&".join([f"{k}={v}" for k, v in form_data.items()])
        response = self.fetch(
            "/form",
            method="POST",
            body=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        self.assertEqual(response.code, 200)
        self.assertIn(b"Thank you, John Doe!", response.body)
        self.assertIn(b"john@example.com", response.body)

    def test_form_post_missing_field(self):
        """Test form submission with missing required field."""
        form_data = {
            "name": "John Doe",
            "email": "john@example.com"
            # Missing 'message' field
        }

        body = "&".join([f"{k}={v}" for k, v in form_data.items()])
        response = self.fetch(
            "/form",
            method="POST",
            body=body,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        self.assertEqual(response.code, 400)
        self.assertIn(b"Error: Missing required field", response.body)

    def test_async_endpoint(self):
        """Test async operations endpoint."""
        response = self.fetch("/async")
        self.assertEqual(response.code, 200)
        self.assertIn(b"Async Operations Demo", response.body)
        self.assertIn(b"Database query completed", response.body)
        self.assertIn(b"Operations completed!", response.body)

    def test_weather_endpoint_default(self):
        """Test weather endpoint with default city."""
        response = self.fetch("/weather")
        self.assertEqual(response.code, 200)
        self.assertIn(b"Weather in London", response.body)
        self.assertIn(b"Temperature:", response.body)
        self.assertIn(b"Description:", response.body)

    def test_weather_endpoint_custom_city(self):
        """Test weather endpoint with custom city."""
        response = self.fetch("/weather?city=Paris")
        self.assertEqual(response.code, 200)
        self.assertIn(b"Weather in Paris", response.body)
        self.assertIn(b"Temperature:", response.body)

    def test_upload_get(self):
        """Test file upload form display."""
        response = self.fetch("/upload")
        self.assertEqual(response.code, 200)
        self.assertIn(b"File Upload Example", response.body)
        self.assertIn(b'type="file"', response.body)
        self.assertIn(b'enctype="multipart/form-data"', response.body)

    def test_upload_post_no_file(self):
        """Test file upload with no file."""
        response = self.fetch(
            "/upload",
            method="POST",
            body="description=test",
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        self.assertEqual(response.code, 400)
        self.assertIn(b"No file uploaded", response.body)

    def test_websocket_test_page(self):
        """Test WebSocket test page loads."""
        response = self.fetch("/websocket")
        self.assertEqual(response.code, 200)
        self.assertIn(b"WebSocket Test", response.body)
        self.assertIn(b"new WebSocket", response.body)

    def test_404_error(self):
        """Test custom 404 error page."""
        response = self.fetch("/nonexistent")
        # The response might be 404 or 405 depending on routing
        self.assertIn(response.code, [404, 405])
        if response.code == 404:
            self.assertIn(b"404 - Page Not Found", response.body)

    def test_static_file_handler(self):
        """Test static file serving."""
        response = self.fetch("/static/tornado-python.png")
        # Static file may or may not exist, but handler should respond
        self.assertIn(response.code, [200, 404])

    def test_method_not_allowed(self):
        """Test method not allowed responses."""
        response = self.fetch("/json", method="POST", body="")
        self.assertEqual(response.code, 405)  # Method Not Allowed


class TestWebSocketHandler(tornado.testing.AsyncHTTPTestCase):
    """Separate test class for WebSocket functionality."""

    def get_app(self):
        """Return the application instance for testing."""
        return make_app()

    def test_websocket_connection(self):
        """Test WebSocket connection (basic connectivity)."""
        # Note: Full WebSocket testing requires more complex setup
        # This is a placeholder for WebSocket testing structure
        pass


class TestUtilityFunctions(unittest.TestCase):
    """Test utility functions and patterns."""

    def test_app_creation(self):
        """Test that the app can be created without errors."""
        app = make_app()
        self.assertIsInstance(app, tornado.web.Application)

    def test_app_settings(self):
        """Test application settings are properly configured."""
        app = make_app()
        self.assertTrue(app.settings.get("debug"))
        self.assertTrue(app.settings.get("autoreload"))
        self.assertIn("template_path", app.settings)
        self.assertIn("static_path", app.settings)

    def test_url_patterns(self):
        """Test URL patterns are properly configured."""
        app = make_app()

        # Check that we have URL patterns configured
        self.assertGreater(len(app.default_router.rules), 0)

        # Check for specific patterns by examining the handlers
        found_patterns = []
        for rule in app.default_router.rules:
            if hasattr(rule, 'regex'):
                found_patterns.append(rule.regex.pattern)
            elif hasattr(rule, 'pattern'):
                found_patterns.append(rule.pattern)

        # Just verify we have some patterns
        self.assertGreater(len(found_patterns), 0)


if __name__ == "__main__":
    # Configure test runner
    import logging
    logging.getLogger().setLevel(logging.ERROR)  # Reduce log noise during tests

    # Run tests
    unittest.main(verbosity=2)
