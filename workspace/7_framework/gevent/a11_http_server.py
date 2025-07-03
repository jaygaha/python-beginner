import logging
import time
import json
from typing import Callable, List, Dict, Any
import gevent
from gevent.pywsgi import WSGIServer
import urllib.parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger(__name__)

class HttpServerConfig:
    """Configuration for HTTP server examples."""
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 8700,
        request_delay: float = 0.1,
        server_timeout: float = 10.0
    ):
        self.host = host
        self.port = port
        self.request_delay = request_delay
        self.server_timeout = server_timeout

class SimpleWsgiServer:
    """Simple WSGI server with basic routing."""
    def __init__(self, config: HttpServerConfig):
        self.config = config
        self.server: WSGIServer | None = None

    def simple_wsgi_app(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """Handles HTTP requests with basic routing."""
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        logger.info(f"Received {method} request for {path}")

        # Simulate processing delay
        gevent.sleep(self.config.request_delay)

        # Define routes
        if path == '/' and method == 'GET':
            status = '200 OK'
            response = {'message': 'Welcome to the simple WSGI server!', 'time': time.time()}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

        elif path == '/health' and method == 'GET':
            status = '200 OK'
            response = {'status': 'healthy', 'uptime': time.time() - self.start_time}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

        else:
            status = '404 Not Found'
            response = {'error': 'Route not found'}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

    def run(self) -> None:
        """Runs the simple WSGI server."""
        logger.info("*** Simple WSGI HTTP Server ***")
        try:
            self.start_time = time.time()
            self.server = WSGIServer((self.config.host, self.config.port), self.simple_wsgi_app)
            logger.info(f"Starting server at http://{self.config.host}:{self.config.port}")
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down simple WSGI server")
            if self.server:
                self.server.stop()
        except Exception as e:
            logger.error(f"Simple WSGI server failed: {e}")
            if self.server:
                self.server.stop()

class PostRequestServer:
    """WSGI server handling POST requests with JSON data."""
    def __init__(self, config: HttpServerConfig):
        self.config = config
        self.server: WSGIServer | None = None

    def post_wsgi_app(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """Handles POST requests with JSON data."""
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        logger.info(f"Received {method} request for {path}")

        if method != 'POST' or path != '/data':
            status = '405 Method Not Allowed'
            response = {'error': 'Only POST to /data is supported'}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
            data = json.loads(request_body) if request_body else {}
            logger.info(f"Received data: {data}")

            # Simulate processing
            gevent.sleep(self.config.request_delay)

            status = '200 OK'
            response = {'received': data, 'processed_at': time.time()}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        except json.JSONDecodeError:
            status = '400 Bad Request'
            response = {'error': 'Invalid JSON data'}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]
        except Exception as e:
            status = '500 Internal Server Error'
            response = {'error': str(e)}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

    def run(self) -> None:
        """Runs the POST request server."""
        logger.info("*** POST Request Server ***")
        try:
            self.server = WSGIServer((self.config.host, self.config.port + 1), self.post_wsgi_app)
            logger.info(f"Starting POST server at http://{self.config.host}:{self.config.port + 1}")
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down POST request server")
            if self.server:
                self.server.stop()
        except Exception as e:
            logger.error(f"POST request server failed: {e}")
            if self.server:
                self.server.stop()

class QueryParamServer:
    """WSGI server handling query parameters."""
    def __init__(self, config: HttpServerConfig):
        self.config = config
        self.server: WSGIServer | None = None

    def query_wsgi_app(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """Handles GET requests with query parameters."""
        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        query_string = environ.get('QUERY_STRING', '')
        logger.info(f"Received {method} request for {path} with query: {query_string}")

        if method != 'GET' or path != '/search':
            status = '405 Method Not Allowed'
            response = {'error': 'Only GET to /search is supported'}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

        # Parse query parameters
        params = urllib.parse.parse_qs(query_string)
        logger.info(f"Parsed query params: {params}")

        # Simulate processing
        gevent.sleep(self.config.request_delay)

        status = '200 OK'
        response = {'query_params': {k: v[0] if len(v) == 1 else v for k, v in params.items()}}
        headers = [('Content-Type', 'application/json')]
        start_response(status, headers)
        return [json.dumps(response).encode('utf-8')]

    def run(self) -> None:
            """Runs the query parameter server."""
            logger.info("*** Query Parameter Server ***")
            try:
                self.server = WSGIServer((self.config.host, self.config.port + 2), self.query_wsgi_app)
                logger.info(f"Starting query server at http://{self.config.host}:{self.config.port + 2}")
                self.server.serve_forever()
            except KeyboardInterrupt:
                logger.info("Shutting down query parameter server")
                if self.server:
                    self.server.stop()
            except Exception as e:
                logger.error(f"Query parameter server failed: {e}")
                if self.server:
                    self.server.stop()

class ErrorHandlingServer:
    """WSGI server with error handling and simulated failures."""
    def __init__(self, config: HttpServerConfig):
        self.config = config
        self.server: WSGIServer | None = None

    def error_wsgi_app(self, environ: Dict[str, Any], start_response: Callable) -> List[bytes]:
        """Handles requests with simulated errors."""
        import random

        method = environ['REQUEST_METHOD']
        path = environ.get('PATH_INFO', '/')
        logger.info(f"Received {method} request for {path}")

        # Simulate processing delay
        gevent.sleep(self.config.request_delay)

        # Define routes with error simulation
        if path == '/success' and method == 'GET':
            status = '200 OK'
            response = {'message': 'Success', 'time': time.time()}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

        elif path == '/error' and method == 'GET':
            if random.random() < 0.3:  # 30% chance of error
                status = '500 Internal Server Error'
                response = {'error': 'Simulated server error'}
                headers = [('Content-Type', 'application/json')]
                start_response(status, headers)
                return [json.dumps(response).encode('utf-8')]
            else:
                status = '200 OK'
                response = {'message': 'No error this time'}
                headers = [('Content-Type', 'application/json')]
                start_response(status, headers)
                return [json.dumps(response).encode('utf-8')]

        else:
            status = '404 Not Found'
            response = {'error': 'Route not found'}
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(response).encode('utf-8')]

    def run(self) -> None:
        """Runs the error handling server."""
        logger.info("*** Error Handling Server ***")
        try:
            self.server = WSGIServer((self.config.host, self.config.port + 3), self.error_wsgi_app)
            logger.info(f"Starting error handling server at http://{self.config.host}:{self.config.port + 3}")
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("Shutting down error handling server")
            if self.server:
                self.server.stop()
        except Exception as e:
            logger.error(f"Error handling server failed: {e}")
            if self.server:
                self.server.stop()

def main():
    """Runs all HTTP server examples sequentially."""
    config = HttpServerConfig()

    # Simple WSGI Server
    simple_server = SimpleWsgiServer(config)
    logger.info("Starting Simple WSGI Server (Ctrl+C to stop)")
    server_greenlet = gevent.spawn(simple_server.run)
    gevent.sleep(config.server_timeout)  # Run for a limited time
    server_greenlet.kill()
    logger.info("Simple WSGI Server stopped\n" + "="*50 + "\n")

    # POST Request Server
    post_server = PostRequestServer(config)
    logger.info("Starting POST Request Server (Ctrl+C to stop)")
    server_greenlet = gevent.spawn(post_server.run)
    gevent.sleep(config.server_timeout)
    server_greenlet.kill()
    logger.info("POST Request Server stopped\n" + "="*50 + "\n")

    # Query Parameter Server
    query_server = QueryParamServer(config)
    logger.info("Starting Query Parameter Server (Ctrl+C to stop)")
    server_greenlet = gevent.spawn(query_server.run)
    gevent.sleep(config.server_timeout)
    server_greenlet.kill()
    logger.info("Query Parameter Server stopped\n" + "="*50 + "\n")

    # Error Handling Server
    error_server = ErrorHandlingServer(config)
    logger.info("Starting Error Handling Server (Ctrl+C to stop)")
    server_greenlet = gevent.spawn(error_server.run)
    gevent.sleep(config.server_timeout)
    server_greenlet.kill()
    logger.info("Error Handling Server stopped\n" + "="*50)

if __name__ == "__main__":
    main()
