#!/usr/bin/env python3
"""
Tornado Web Framework Examples
==============================

This file demonstrates common Tornado patterns and use cases that developers
encounter when building web applications with Tornado.

Run this file to see various examples in action:
    python examples.py
"""

import asyncio
import json
import logging
import os
import tornado.ioloop
import tornado.web
import tornado.httpclient
import tornado.websocket
from datetime import datetime
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Example 1: Basic Handler Patterns ---

class HomeHandler(tornado.web.RequestHandler):
    """Basic GET handler returning HTML."""

    async def get(self):
        self.write("""
        <html>
            <head><title>Tornado Examples</title></head>
            <body>
                <h1>Welcome to Tornado Examples</h1>
                <ul>
                    <li><a href="/json">JSON Response</a></li>
                    <li><a href="/form">Form Example</a></li>
                    <li><a href="/async">Async Operation</a></li>
                    <li><a href="/weather">Weather API</a></li>
                    <li><a href="/upload">File Upload</a></li>
                    <li><a href="/websocket">WebSocket Test</a></li>
                </ul>
            </body>
        </html>
        """)

class JSONHandler(tornado.web.RequestHandler):
    """Handler demonstrating JSON responses."""

    async def get(self):
        data = {
            "message": "Hello from Tornado!",
            "timestamp": datetime.now().isoformat(),
            "method": self.request.method,
            "path": self.request.path,
            "user_agent": self.request.headers.get("User-Agent", "Unknown")
        }

        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data, indent=2))

# --- Example 2: Form Handling ---

class FormHandler(tornado.web.RequestHandler):
    """Handler demonstrating form processing."""

    async def get(self):
        """Display the form."""
        self.write("""
        <html>
            <head><title>Form Example</title></head>
            <body>
                <h2>Contact Form</h2>
                <form method="post" action="/form">
                    <p>
                        <label>Name:</label><br>
                        <input type="text" name="name" required>
                    </p>
                    <p>
                        <label>Email:</label><br>
                        <input type="email" name="email" required>
                    </p>
                    <p>
                        <label>Message:</label><br>
                        <textarea name="message" rows="5" cols="40" required></textarea>
                    </p>
                    <p>
                        <input type="submit" value="Submit">
                    </p>
                </form>
                <a href="/">Back to Home</a>
            </body>
        </html>
        """)

    async def post(self):
        """Process form submission."""
        try:
            name = self.get_argument("name")
            email = self.get_argument("email")
            message = self.get_argument("message")

            # In a real app, you'd save this to a database
            logger.info(f"Form submission: {name} <{email}> - {message}")

            self.write(f"""
            <html>
                <head><title>Form Submitted</title></head>
                <body>
                    <h2>Thank you, {name}!</h2>
                    <p>Your message has been received.</p>
                    <p><strong>Email:</strong> {email}</p>
                    <p><strong>Message:</strong> {message}</p>
                    <a href="/form">Submit Another</a> |
                    <a href="/">Back to Home</a>
                </body>
            </html>
            """)

        except tornado.web.MissingArgumentError as e:
            self.set_status(400)
            self.write(f"<h2>Error: Missing required field - {e.arg_name}</h2>")

# --- Example 3: Async Operations ---

class AsyncHandler(tornado.web.RequestHandler):
    """Handler demonstrating async operations."""

    async def get(self):
        """Perform multiple async operations."""
        self.write("<h2>Async Operations Demo</h2>")
        self.write("<p>Starting async operations...</p>")

        # Simulate async database query
        await self.simulate_db_query()

        # Simulate async API call
        result = await self.simulate_api_call()

        self.write(f"<p>Operations completed! Result: {result}</p>")
        self.write('<a href="/">Back to Home</a>')

    async def simulate_db_query(self):
        """Simulate an async database query."""
        await asyncio.sleep(0.5)  # Simulate network delay
        self.write("<p>✓ Database query completed</p>")

    async def simulate_api_call(self):
        """Simulate an async API call."""
        await asyncio.sleep(0.3)  # Simulate network delay
        return {"status": "success", "data": "API response"}

# --- Example 4: HTTP Client (External API) ---

class WeatherHandler(tornado.web.RequestHandler):
    """Handler demonstrating HTTP client usage."""

    async def get(self):
        """Fetch weather data from an external API."""
        city = self.get_argument("city", "London")

        try:
            # Create HTTP client
            http_client = tornado.httpclient.AsyncHTTPClient()

            # Note: This is a mock API endpoint for demonstration
            # In production, you'd use a real weather API with an API key
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY"

            # For demo purposes, simulate a weather response
            weather_data = await self.simulate_weather_api(city)

            self.write(f"""
            <html>
                <head><title>Weather for {city}</title></head>
                <body>
                    <h2>Weather in {city}</h2>
                    <p><strong>Temperature:</strong> {weather_data['temp']}°C</p>
                    <p><strong>Description:</strong> {weather_data['description']}</p>
                    <p><strong>Humidity:</strong> {weather_data['humidity']}%</p>
                    <form method="get" action="/weather">
                        <input type="text" name="city" placeholder="Enter city name" value="{city}">
                        <input type="submit" value="Get Weather">
                    </form>
                    <a href="/">Back to Home</a>
                </body>
            </html>
            """)

        except Exception as e:
            self.set_status(500)
            self.write(f"<h2>Error fetching weather: {str(e)}</h2>")

    async def simulate_weather_api(self, city: str) -> Dict[str, Any]:
        """Simulate weather API response."""
        await asyncio.sleep(0.2)  # Simulate network delay

        # Mock weather data
        weather_data = {
            "London": {"temp": 15, "description": "Cloudy", "humidity": 78},
            "Paris": {"temp": 18, "description": "Sunny", "humidity": 65},
            "Tokyo": {"temp": 22, "description": "Rainy", "humidity": 82},
            "New York": {"temp": 12, "description": "Windy", "humidity": 71}
        }

        return weather_data.get(city, {
            "temp": 20,
            "description": "Unknown",
            "humidity": 50
        })

# --- Example 5: File Upload ---

class UploadHandler(tornado.web.RequestHandler):
    """Handler demonstrating file upload."""

    async def get(self):
        """Display upload form."""
        self.write("""
        <html>
            <head><title>File Upload</title></head>
            <body>
                <h2>File Upload Example</h2>
                <form method="post" enctype="multipart/form-data" action="/upload">
                    <p>
                        <label>Choose file:</label><br>
                        <input type="file" name="file" required>
                    </p>
                    <p>
                        <label>Description:</label><br>
                        <input type="text" name="description" placeholder="Optional description">
                    </p>
                    <p>
                        <input type="submit" value="Upload">
                    </p>
                </form>
                <a href="/">Back to Home</a>
            </body>
        </html>
        """)

    async def post(self):
        """Handle file upload."""
        try:
            if "file" not in self.request.files:
                self.set_status(400)
                self.write("<h2>No file uploaded</h2>")
                return

            file_info = self.request.files["file"][0]
            filename = file_info["filename"]
            content_type = file_info["content_type"]
            body = file_info["body"]

            description = self.get_argument("description", "No description")

            # In a real app, you'd save the file to disk or cloud storage
            # For demo, we'll just show the file info

            self.write(f"""
            <html>
                <head><title>Upload Success</title></head>
                <body>
                    <h2>File Uploaded Successfully!</h2>
                    <p><strong>Filename:</strong> {filename}</p>
                    <p><strong>Content Type:</strong> {content_type}</p>
                    <p><strong>File Size:</strong> {len(body)} bytes</p>
                    <p><strong>Description:</strong> {description}</p>
                    <a href="/upload">Upload Another</a> |
                    <a href="/">Back to Home</a>
                </body>
            </html>
            """)

        except Exception as e:
            self.set_status(500)
            self.write(f"<h2>Upload Error: {str(e)}</h2>")

# --- Example 6: WebSocket ---

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    """WebSocket handler for real-time communication."""

    clients = set()

    def open(self):
        """Called when WebSocket connection is opened."""
        self.clients.add(self)
        logger.info(f"WebSocket opened. Total clients: {len(self.clients)}")
        self.write_message({"type": "welcome", "message": "Connected to WebSocket!"})

    def on_message(self, message):
        """Called when a message is received."""
        try:
            data = json.loads(message)
            logger.info(f"Received: {data}")

            # Echo the message back to all connected clients
            response = {
                "type": "echo",
                "message": data.get("message", ""),
                "timestamp": datetime.now().isoformat()
            }

            for client in self.clients:
                client.write_message(response)

        except json.JSONDecodeError:
            self.write_message({"type": "error", "message": "Invalid JSON"})

    def on_close(self):
        """Called when WebSocket connection is closed."""
        self.clients.remove(self)
        logger.info(f"WebSocket closed. Total clients: {len(self.clients)}")

class WebSocketTestHandler(tornado.web.RequestHandler):
    """Handler serving WebSocket test page."""

    async def get(self):
        self.write("""
        <html>
            <head><title>WebSocket Test</title></head>
            <body>
                <h2>WebSocket Test</h2>
                <div id="messages"></div>
                <input type="text" id="messageInput" placeholder="Type a message...">
                <button onclick="sendMessage()">Send</button>
                <button onclick="disconnect()">Disconnect</button>
                <br><br>
                <a href="/">Back to Home</a>

                <script>
                    const ws = new WebSocket('ws://localhost:8888/ws');
                    const messages = document.getElementById('messages');

                    ws.onmessage = function(event) {
                        const data = JSON.parse(event.data);
                        const div = document.createElement('div');
                        div.innerHTML = `<strong>${data.type}:</strong> ${data.message}`;
                        messages.appendChild(div);
                    };

                    function sendMessage() {
                        const input = document.getElementById('messageInput');
                        const message = input.value;
                        if (message) {
                            ws.send(JSON.stringify({message: message}));
                            input.value = '';
                        }
                    }

                    function disconnect() {
                        ws.close();
                    }

                    // Send message on Enter key
                    document.getElementById('messageInput').addEventListener('keypress', function(e) {
                        if (e.key === 'Enter') {
                            sendMessage();
                        }
                    });
                </script>
            </body>
        </html>
        """)

# --- Example 7: Custom Error Handler ---

class CustomErrorHandler(tornado.web.RequestHandler):
    """Custom error handler for 404 and other errors."""

    def prepare(self):
        """Called before any HTTP method."""
        # This method is called before get, post, etc.
        pass

    def write_error(self, status_code, **kwargs):
        """Custom error page."""
        if status_code == 404:
            self.write("""
            <html>
                <head><title>Page Not Found</title></head>
                <body>
                    <h1>404 - Page Not Found</h1>
                    <p>The page you're looking for doesn't exist.</p>
                    <a href="/">Go Home</a>
                </body>
            </html>
            """)
        else:
            self.write(f"""
            <html>
                <head><title>Error {status_code}</title></head>
                <body>
                    <h1>Error {status_code}</h1>
                    <p>Something went wrong.</p>
                    <a href="/">Go Home</a>
                </body>
            </html>
            """)

# --- Application Setup ---

def make_app():
    """Create and configure the Tornado application."""

    settings = {
        "debug": True,
        "autoreload": True,
        "default_handler_class": CustomErrorHandler,
        "template_path": os.path.join(os.path.dirname(__file__), "templates"),
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
    }

    return tornado.web.Application([
        (r"/", HomeHandler),
        (r"/json", JSONHandler),
        (r"/form", FormHandler),
        (r"/async", AsyncHandler),
        (r"/weather", WeatherHandler),
        (r"/upload", UploadHandler),
        (r"/websocket", WebSocketTestHandler),
        (r"/ws", WebSocketHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
    ], **settings)

# --- Main Application ---

async def main():
    """Main application entry point."""
    app = make_app()
    port = 8888

    app.listen(port)
    logger.info(f"🚀 Tornado Examples Server started on http://localhost:{port}")
    logger.info("📖 Available examples:")
    logger.info("   • http://localhost:8888/ - Home page with all examples")
    logger.info("   • http://localhost:8888/json - JSON response")
    logger.info("   • http://localhost:8888/form - Form handling")
    logger.info("   • http://localhost:8888/async - Async operations")
    logger.info("   • http://localhost:8888/weather - External API example")
    logger.info("   • http://localhost:8888/upload - File upload")
    logger.info("   • http://localhost:8888/websocket - WebSocket test")
    logger.info("Press Ctrl+C to stop the server")

    # Keep the server running
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
