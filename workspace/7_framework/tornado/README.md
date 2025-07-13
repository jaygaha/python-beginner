# Tornado Web Framework - Basic Implementation

A comprehensive guide to building web applications with Python's Tornado framework, featuring modern async/await patterns, template rendering, static file serving, and graceful shutdown handling.

## Overview

Tornado is a Python web framework and asynchronous networking library that excels at handling thousands of simultaneous connections. This implementation demonstrates core Tornado concepts including:

- **Asynchronous Request Handlers** - Modern async/await pattern usage
- **URL Routing** - Clean URL pattern mapping
- **Template Rendering** - Server-side HTML generation
- **Static File Serving** - CSS, JavaScript, and image handling
- **Graceful Shutdown** - Proper signal handling for production deployment

## Project Structure

```
tornado/
├── basic.py              # Main application file
├── examples.py           # Comprehensive examples and patterns
├── requirements.txt      # Python dependencies
├── templates/           # HTML templates
│   └── hello.html      # Sample template
├── static/             # Static assets
│   └── tornado-python.png
├── i18n/               # Internationalization implementation
│   ├── app.py          # Multi-language web application
│   ├── README.md       # i18n documentation
│   ├── locale/         # Translation files
│   │   ├── en_US.csv   # English translations
│   │   └── ja_JP.csv   # Japanese translations
│   └── templates/      # Localized templates
│       └── index.html  # Multi-language template
└── rest_api_app/       # REST API implementation
    ├── app.py
    ├── test_app.py
    └── README.md
```

## Features

### Core Handlers

- **MainHandler (`/`)** - Simple "Hello World" endpoint
- **GreetHandler (`/hello/{name}`)** - Parameterized URLs with template rendering
- **AsyncHandler (`/async`)** - Demonstrates non-blocking async operations
- **StaticFileHandler (`/static/`)** - Serves static files (images, CSS, JS)

### Modern Implementation Features

- **Async/Await Pattern** - All handlers use modern async syntax
- **Type Hints** - Full type annotation support
- **Centralized Configuration** - Easy settings management
- **Signal Handling** - Graceful shutdown on SIGINT/SIGTERM
- **Logging Integration** - Proper logging setup
- **Debug Mode** - Auto-reloading and detailed error pages
- **Internationalization (i18n)** - Multi-language support with locale switching

## Requirements

- Python 3.7+
- Tornado 6.0+

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or install Tornado directly:
```bash
pip install tornado
```

## Usage

### Starting the Server

Run the application:
```bash
python basic.py
```

The server will start on `http://localhost:8888`

### Running Examples

For a more comprehensive demonstration of Tornado features:

```bash
python examples.py
```

This will start an enhanced server with additional examples including:
- Form handling
- File uploads
- WebSocket connections
- External API integration
- Error handling patterns

### Available Endpoints

#### 1. Root Endpoint
```
GET /
```
Returns a simple "Hello, Modern Tornado World!" message.

**Example:**
```bash
curl http://localhost:8888/
```

#### 2. Greeting with Template
```
GET /hello/{name}
```
Renders an HTML template with the provided name parameter.

**Example:**
```bash
curl http://localhost:8888/hello/Alice
```

**Response:**
```html
<html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello, Alice!</h1>
    </body>
</html>
```

#### 3. Async Operation
```
GET /async
```
Demonstrates non-blocking asynchronous operations with a 1-second delay.

**Example:**
```bash
curl http://localhost:8888/async
```

#### 4. Static Files
```
GET /static/{filename}
```
Serves static files from the `static/` directory.

**Example:**
```bash
curl http://localhost:8888/static/tornado-python.png
```

## Code Architecture

### Application Configuration

```python
SETTINGS = {
    "template_path": os.path.join(os.path.dirname(__file__), "templates"),
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,  # Enable auto-reloading and detailed error pages
}
```

### Request Handler Pattern

```python
class MainHandler(tornado.web.RequestHandler):
    """A simple handler for the root URL."""
    async def get(self) -> None:
        self.write("Hello, Modern Tornado World!")
```

### URL Routing

```python
def make_app() -> tornado.web.Application:
    """Creates and returns the Tornado application instance."""
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/hello/([^/]+)", GreetHandler),
        (r"/async", AsyncHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": SETTINGS["static_path"]}),
    ], **SETTINGS)
```

### Graceful Shutdown

```python
def sig_handler(sig: int, frame) -> None:
    """Signal handler to initiate a graceful shutdown."""
    logging.info(f"Caught signal: {sig}. Shutting down...")
    ioloop = tornado.ioloop.IOLoop.current()
    ioloop.add_callback_from_signal(ioloop.stop)
```

## Templates

### Basic Template Structure

The `hello.html` template demonstrates Tornado's template engine:

```html
<html>
    <head>
        <title>Hello</title>
    </head>
    <body>
        <h1>Hello, {{ name }}!</h1>
    </body>
</html>
```

### Template Features

- **Variable Interpolation** - `{{ variable }}`
- **Control Structures** - `{% if %}`, `{% for %}`, `{% while %}`
- **Template Inheritance** - `{% extends %}`, `{% block %}`
- **Auto-escaping** - XSS protection by default

## Static File Serving

Static files are served from the `static/` directory and accessible via `/static/` URL prefix:

- **Images** - PNG, JPG, GIF, SVG
- **Stylesheets** - CSS files
- **JavaScript** - JS files
- **Other Assets** - Fonts, documents, etc.

## Development Features

### Debug Mode

When `debug=True` is set:
- **Auto-reloading** - Server restarts on file changes
- **Detailed Error Pages** - Stack traces in browser
- **Template Auto-reloading** - No server restart needed for template changes

### Logging

The application includes comprehensive logging:
- **Startup Messages** - Server URL and shutdown instructions
- **Signal Handling** - Graceful shutdown notifications
- **Request Logging** - Automatic HTTP request logging

## Testing

### Manual Testing

Test endpoints using curl:

```bash
# Test root endpoint
curl http://localhost:8888/

# Test parameterized endpoint
curl http://localhost:8888/hello/World

# Test async endpoint
curl http://localhost:8888/async

# Test static file serving
curl http://localhost:8888/static/tornado-python.png
```

### Browser Testing

Open your browser and navigate to:
- `http://localhost:8888/` - Simple text response
- `http://localhost:8888/hello/YourName` - HTML template
- `http://localhost:8888/async` - Async operation
- `http://localhost:8888/static/tornado-python.png` - Static image

## Production Considerations

### Performance

- **Async Operations** - Use `await` for I/O operations
- **Connection Pooling** - Reuse database connections
- **Caching** - Implement response caching where appropriate

### Security

- **Template Escaping** - Enabled by default
- **HTTPS** - Use SSL certificates in production
- **Input Validation** - Validate all user inputs
- **CORS** - Configure Cross-Origin Resource Sharing

### Deployment

- **Process Management** - Use supervisord or systemd
- **Reverse Proxy** - Nginx for static files and load balancing
- **Environment Variables** - Externalize configuration
- **Logging** - Structured logging for production

## Examples and Patterns

### Comprehensive Examples (`examples.py`)

The `examples.py` file demonstrates advanced Tornado patterns:

**Available Examples:**
- **Form Handling** - `/form` - Complete form processing with validation
- **JSON APIs** - `/json` - RESTful JSON responses with headers
- **Async Operations** - `/async` - Non-blocking database and API calls
- **File Uploads** - `/upload` - Multipart form data handling
- **WebSocket** - `/websocket` - Real-time bidirectional communication
- **External APIs** - `/weather` - HTTP client usage with external services
- **Error Handling** - Custom 404 and error pages

**Key Features Demonstrated:**
- Modern async/await patterns
- HTTP client usage with `tornado.httpclient`
- WebSocket real-time communication
- File upload handling
- Form validation and processing
- Custom error pages
- JSON API responses
- External API integration

### Usage Patterns

**Error Handling:**
```python
async def get(self):
    try:
        result = await some_async_operation()
        self.write(result)
    except Exception as e:
        self.set_status(500)
        self.write({"error": str(e)})
```

**JSON Responses:**
```python
async def get(self):
    data = {"message": "Hello, JSON!"}
    self.set_header("Content-Type", "application/json")
    self.write(json.dumps(data))
```

**WebSocket Communication:**
```python
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.write_message({"type": "welcome"})
    
    def on_message(self, message):
        data = json.loads(message)
        self.write_message({"echo": data})
```

## Related Projects

- **REST API** - See `rest_api_app/` for a complete REST API implementation
- **Internationalization** - See `i18n/` for multi-language web application with locale switching
- **Advanced Templates** - Explore template inheritance and macros
- **Database Integration** - Add SQLAlchemy or Motor for database support
- **Authentication** - Implement user authentication and authorization

## Internationalization (i18n)

The `i18n/` directory contains a comprehensive implementation of internationalization in Tornado, featuring:

### Features

- **Multi-language Support** - English (US) and Japanese translations
- **URL-based Locale Routing** - `/en_US/about-us` and `/ja_JP/about-us` patterns
- **Dynamic Language Switching** - Flag-based locale switcher with emoji flags
- **CSV Translation Files** - Simple translation management with parameterized content
- **Template Localization** - Full template translation with `{{ _("key") }}` syntax
- **Fallback Handling** - Automatic fallback to English for unsupported locales

### Quick Start

```bash
# Navigate to i18n directory
cd i18n/

# Run the internationalized application
python app.py

# Access in different languages
# English: http://localhost:8880/en_US/about-us
# Japanese: http://localhost:8880/ja_JP/about-us
```

### Translation Management

Translations are stored in CSV format for easy management:

```csv
# locale/en_US.csv
home,Home
about,About
created-by,Created by %(author)s

# locale/ja_JP.csv
home,ホーム
about,について
created-by,%(author)s によって作成されました
```

### Template Usage

Templates use Tornado's built-in translation syntax:

```html
<nav>
    <a href="#">{{ _("home") }}</a>
    <a href="#">{{ _("about") }}</a>
</nav>
<p>{{ _("created-by") % {"author": author} }}</p>
```

For detailed implementation guide and advanced features, see the complete documentation in `i18n/README.md`.

## Common Patterns

### Error Handling

```python
class ErrorHandler(tornado.web.RequestHandler):
    async def get(self):
        try:
            # Your logic here
            result = await some_async_operation()
            self.write(result)
        except Exception as e:
            self.set_status(500)
            self.write({"error": str(e)})
```

### JSON Responses

```python
class JSONHandler(tornado.web.RequestHandler):
    async def get(self):
        data = {"message": "Hello, JSON!"}
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(data))
```

### Request Parsing

```python
class PostHandler(tornado.web.RequestHandler):
    async def post(self):
        # Parse JSON body
        data = json.loads(self.request.body)
        
        # Access form data
        name = self.get_argument("name")
        
        # Process and respond
        self.write(f"Hello, {name}!")
```

## Resources

- **Official Documentation** - https://tornadoweb.org/
- **GitHub Repository** - https://github.com/tornadoweb/tornado
- **Community** - Tornado Google Group and Stack Overflow
- **Examples** - https://github.com/tornadoweb/tornado/tree/master/demos

## License

This implementation is provided as educational material. Tornado itself is licensed under the Apache License 2.0.