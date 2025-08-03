from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass, field
from collections import defaultdict
import time
import logging
import uuid
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class RateLimitConfig:
    """Configuration for rate limiting."""
    calls: int = 100
    period: int = 60
    cleanup_interval: int = 300  # Clean old entries every 5 minutes


@dataclass
class ClientRateData:
    """Rate limiting data for a client."""
    requests: List[float] = field(default_factory=list)
    last_cleanup: float = field(default_factory=time.time)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging requests and responses with structured data."""

    def __init__(self, app, log_body: bool = False, max_body_size: int = 1000):
        super().__init__(app)
        self.log_body = log_body
        self.max_body_size = max_body_size

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate request ID
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Log request details
        start_time = time.time()
        client_ip = self._get_client_ip(request)

        log_data = {
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": client_ip,
            "user_agent": request.headers.get("user-agent", "unknown")
        }

        if self.log_body and request.method in ["POST", "PUT", "PATCH"]:
            try:
                body = await request.body()
                if len(body) <= self.max_body_size:
                    log_data["request_body"] = body.decode("utf-8")[:self.max_body_size]
            except Exception:
                log_data["request_body"] = "<unable to decode>"

        logger.info(f"Incoming request: {json.dumps(log_data)}")

        # Process request
        try:
            response = await call_next(request)
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(f"Request {request_id} failed: {str(e)} (Time: {process_time:.4f}s)")
            raise

        # Calculate processing time and add headers
        process_time = time.time() - start_time
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Process-Time"] = f"{process_time:.4f}"

        # Log response
        logger.info(
            f"Request completed: {json.dumps({
                'request_id': request_id,
                'status_code': response.status_code,
                'process_time': f'{process_time:.4f}s'
            })}"
        )

        return response

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP considering proxy headers."""
        # Check for X-Forwarded-For header (common with load balancers)
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        # Check for X-Real-IP header
        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fall back to direct client IP
        return request.client.host if request.client else "unknown"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers."""

    def __init__(self, app, custom_headers: Optional[Dict[str, str]] = None):
        super().__init__(app)
        self.default_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), camera=(), microphone=()"
        }
        self.custom_headers = custom_headers or {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Add default security headers
        for header, value in self.default_headers.items():
            response.headers[header] = value

        # Add custom headers
        for header, value in self.custom_headers.items():
            response.headers[header] = value

        return response


class RateLimitingMiddleware(BaseHTTPMiddleware):
    """Enhanced rate limiting middleware with automatic cleanup."""

    def __init__(self, app, config: Optional[RateLimitConfig] = None):
        super().__init__(app)
        self.config = config or RateLimitConfig()
        self.clients: Dict[str, ClientRateData] = defaultdict(ClientRateData)
        self._last_global_cleanup = time.time()

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        client_ip = self._get_client_ip(request)
        current_time = time.time()

        # Perform periodic cleanup
        await self._cleanup_if_needed(current_time)

        # Get or create client data
        client_data = self.clients[client_ip]

        # Clean old entries for this client
        client_data.requests = [
            req_time for req_time in client_data.requests
            if current_time - req_time < self.config.period
        ]

        # Check rate limit
        if len(client_data.requests) >= self.config.calls:
            oldest_request = min(client_data.requests)
            retry_after = int(self.config.period - (current_time - oldest_request))

            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Rate limit exceeded",
                    "message": f"Maximum {self.config.calls} requests per {self.config.period} seconds",
                    "retry_after": retry_after
                },
                headers={"Retry-After": str(retry_after)}
            )

        # Add current request
        client_data.requests.append(current_time)
        return await call_next(request)

    async def _cleanup_if_needed(self, current_time: float):
        """Perform global cleanup of old client entries."""
        if current_time - self._last_global_cleanup > self.config.cleanup_interval:
            self._last_global_cleanup = current_time

            # Remove clients with no recent requests
            clients_to_remove = []
            for client_ip, client_data in self.clients.items():
                if not client_data.requests or current_time - max(client_data.requests) > self.config.period * 2:
                    clients_to_remove.append(client_ip)

            for client_ip in clients_to_remove:
                del self.clients[client_ip]

            if clients_to_remove:
                logger.info(f"Cleaned up {len(clients_to_remove)} inactive rate limit entries")

    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP considering proxy headers."""
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"


class RequestSizeMiddleware(BaseHTTPMiddleware):
    """Middleware for enforcing request size limits."""

    def __init__(self, app, max_size: int = 1024 * 1024, exclude_paths: Optional[List[str]] = None):
        super().__init__(app)
        self.max_size = max_size
        self.exclude_paths = set(exclude_paths or [])

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip size check for excluded paths
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        content_length = request.headers.get("content-length")

        if content_length:
            size = int(content_length)
            if size > self.max_size:
                logger.warning(f"Request size {size} exceeds limit {self.max_size} for {request.url.path}")
                return JSONResponse(
                    status_code=413,
                    content={
                        "error": "Request too large",
                        "message": f"Maximum request size is {self._format_size(self.max_size)}",
                        "received_size": self._format_size(size)
                    }
                )

        return await call_next(request)

    def _format_size(self, size_bytes: int) -> str:
        """Format byte size to human readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes = size_bytes // 1024
        return f"{size_bytes:.1f} TB"


class ResponseCompressionMiddleware(BaseHTTPMiddleware):
    """Middleware for response compression."""

    def __init__(self, app, minimum_size: int = 1000, compression_level: int = 6):
        super().__init__(app)
        self.minimum_size = minimum_size
        self.compression_level = compression_level

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        response = await call_next(request)

        # Check if client accepts gzip
        accept_encoding = request.headers.get("accept-encoding", "")
        if "gzip" not in accept_encoding.lower():
            return response

        # Check content type
        content_type = response.headers.get("content-type", "")
        if not self._should_compress(content_type):
            return response

        # For demonstration - in production, use FastAPI's GZipMiddleware or implement actual compression
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Vary"] = "Accept-Encoding"

        return response

    def _should_compress(self, content_type: str) -> bool:
        """Determine if content type should be compressed."""
        compressible_types = [
            "application/json",
            "application/javascript",
            "text/html",
            "text/css",
            "text/plain",
            "text/xml"
        ]
        return any(ct in content_type.lower() for ct in compressible_types)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Enhanced error handling middleware with detailed logging."""

    def __init__(self, app, include_debug_info: bool = False):
        super().__init__(app)
        self.include_debug_info = include_debug_info

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            request_id = getattr(request.state, 'request_id', str(uuid.uuid4()))

            # Log detailed error information
            error_data = {
                "request_id": request_id,
                "error_type": type(e).__name__,
                "error_message": str(e),
                "path": request.url.path,
                "method": request.method,
                "client_ip": request.client.host if request.client else "unknown"
            }

            logger.error(f"Unhandled exception: {json.dumps(error_data)}", exc_info=True)

            # Prepare response content
            response_content = {
                "error": "Internal Server Error",
                "message": "An unexpected error occurred",
                "request_id": request_id
            }

            # Include debug info if enabled (only for development)
            if self.include_debug_info:
                response_content["debug"] = {
                    "error_type": type(e).__name__,
                    "error_message": str(e)
                }

            return JSONResponse(
                status_code=500,
                content=response_content
            )


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware for handling correlation IDs across services."""

    def __init__(self, app, header_name: str = "X-Correlation-ID"):
        super().__init__(app)
        self.header_name = header_name

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get correlation ID from header or generate new one
        correlation_id = request.headers.get(self.header_name.lower()) or str(uuid.uuid4())

        # Store in request state
        request.state.correlation_id = correlation_id

        # Process request
        response = await call_next(request)

        # Add correlation ID to response
        response.headers[self.header_name] = correlation_id

        return response


# Configuration functions
def get_cors_origins() -> List[str]:
    """Get CORS origins configuration."""
    return [
        "http://localhost:3000",   # React dev server
        "http://localhost:8080",   # Vue dev server
        "http://localhost:5173",   # Vite dev server
        "https://myapp.com",       # Production frontend
        "https://admin.myapp.com", # Admin panel
        "https://*.myapp.com"      # Subdomains
    ]


def get_trusted_hosts() -> List[str]:
    """Get trusted hosts configuration."""
    return [
        "localhost",
        "127.0.0.1",
        "*.myapp.com",
        "myapp.com"
    ]
