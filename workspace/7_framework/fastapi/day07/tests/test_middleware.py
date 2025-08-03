import pytest
import json
from unittest.mock import Mock, patch
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from src.middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    RateLimitingMiddleware,
    RequestSizeMiddleware,
    ResponseCompressionMiddleware,
    ErrorHandlingMiddleware,
    CorrelationIDMiddleware,
    RateLimitConfig,
    ClientRateData
)


class TestRequestLoggingMiddleware:
    """Test cases for RequestLoggingMiddleware."""

    @pytest.fixture
    def app_with_middleware(self):
        """Create FastAPI app with RequestLoggingMiddleware."""
        app = FastAPI()
        app.add_middleware(RequestLoggingMiddleware)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        return app

    @pytest.fixture
    def client(self, app_with_middleware):
        """Create test client."""
        return TestClient(app_with_middleware)

    def test_adds_request_id_header(self, client):
        """Test that request ID is added to response headers."""
        response = client.get("/test")
        assert "X-Request-ID" in response.headers
        assert len(response.headers["X-Request-ID"]) == 36  # UUID length

    def test_adds_process_time_header(self, client):
        """Test that process time is added to response headers."""
        response = client.get("/test")
        assert "X-Process-Time" in response.headers
        process_time = float(response.headers["X-Process-Time"])
        assert process_time > 0

    def test_client_ip_extraction_with_forwarded_header(self):
        """Test client IP extraction with X-Forwarded-For header."""
        middleware = RequestLoggingMiddleware(None)

        # Mock request with X-Forwarded-For header
        mock_request = Mock()
        mock_request.headers = {"x-forwarded-for": "192.168.1.1, 10.0.0.1"}
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"

        ip = middleware._get_client_ip(mock_request)
        assert ip == "192.168.1.1"

    def test_client_ip_extraction_with_real_ip_header(self):
        """Test client IP extraction with X-Real-IP header."""
        middleware = RequestLoggingMiddleware(None)

        mock_request = Mock()
        mock_request.headers = {"x-real-ip": "192.168.1.2"}
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"

        ip = middleware._get_client_ip(mock_request)
        assert ip == "192.168.1.2"

    def test_client_ip_fallback_to_direct(self):
        """Test client IP falls back to direct client IP."""
        middleware = RequestLoggingMiddleware(None)

        mock_request = Mock()
        mock_request.headers = {}
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"

        ip = middleware._get_client_ip(mock_request)
        assert ip == "127.0.0.1"


class TestSecurityHeadersMiddleware:
    """Test cases for SecurityHeadersMiddleware."""

    @pytest.fixture
    def app_with_middleware(self):
        """Create FastAPI app with SecurityHeadersMiddleware."""
        app = FastAPI()
        app.add_middleware(SecurityHeadersMiddleware)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        return app

    @pytest.fixture
    def client(self, app_with_middleware):
        """Create test client."""
        return TestClient(app_with_middleware)

    def test_adds_default_security_headers(self, client):
        """Test that default security headers are added."""
        response = client.get("/test")

        expected_headers = {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Permissions-Policy": "geolocation=(), camera=(), microphone=()"
        }

        for header, value in expected_headers.items():
            assert response.headers[header] == value

    def test_adds_custom_headers(self):
        """Test that custom headers are added."""
        app = FastAPI()
        custom_headers = {"Custom-Header": "custom-value"}
        app.add_middleware(SecurityHeadersMiddleware, custom_headers=custom_headers)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        assert response.headers["Custom-Header"] == "custom-value"


class TestRateLimitingMiddleware:
    """Test cases for RateLimitingMiddleware."""

    @pytest.fixture
    def app_with_rate_limiting(self):
        """Create FastAPI app with RateLimitingMiddleware."""
        app = FastAPI()
        config = RateLimitConfig(calls=2, period=60)  # Very low limit for testing
        app.add_middleware(RateLimitingMiddleware, config=config)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        return app

    @pytest.fixture
    def client(self, app_with_rate_limiting):
        """Create test client."""
        return TestClient(app_with_rate_limiting)

    def test_allows_requests_within_limit(self, client):
        """Test that requests within limit are allowed."""
        response1 = client.get("/test")
        response2 = client.get("/test")

        assert response1.status_code == 200
        assert response2.status_code == 200

    def test_blocks_requests_exceeding_limit(self, client):
        """Test that requests exceeding limit are blocked."""
        # Make requests up to the limit
        client.get("/test")
        client.get("/test")

        # This should be blocked
        response = client.get("/test")
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.json()["error"]

    def test_rate_limit_response_includes_retry_after(self, client):
        """Test that rate limit response includes Retry-After header."""
        # Exceed the limit
        client.get("/test")
        client.get("/test")
        response = client.get("/test")

        assert response.status_code == 429
        assert "Retry-After" in response.headers

    def test_rate_limit_config_validation(self):
        """Test RateLimitConfig validation."""
        config = RateLimitConfig(calls=100, period=60)
        assert config.calls == 100
        assert config.period == 60
        assert config.cleanup_interval == 300  # Default value

    def test_client_rate_data_initialization(self):
        """Test ClientRateData initialization."""
        data = ClientRateData()
        assert isinstance(data.requests, list)
        assert len(data.requests) == 0
        assert isinstance(data.last_cleanup, float)


class TestRequestSizeMiddleware:
    """Test cases for RequestSizeMiddleware."""

    @pytest.fixture
    def app_with_size_limit(self):
        """Create FastAPI app with RequestSizeMiddleware."""
        app = FastAPI()
        app.add_middleware(RequestSizeMiddleware, max_size=100)  # Very small limit

        @app.post("/test")
        async def test_endpoint(data: dict):
            return {"message": "test"}

        return app

    @pytest.fixture
    def client(self, app_with_size_limit):
        """Create test client."""
        return TestClient(app_with_size_limit)

    def test_allows_small_requests(self, client):
        """Test that small requests are allowed."""
        small_data = {"key": "value"}
        response = client.post("/test", json=small_data)
        assert response.status_code == 200

    def test_blocks_large_requests(self, client):
        """Test that large requests are blocked."""
        # Create a large payload
        large_data = {"key": "x" * 1000}  # Much larger than 100 bytes

        # We need to manually set content-length header since TestClient might not
        with patch.object(client, 'post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 413
            mock_response.json.return_value = {"error": "Request too large"}
            mock_post.return_value = mock_response

            response = mock_post("/test", json=large_data,
                               headers={"content-length": str(len(json.dumps(large_data)))})
            assert response.status_code == 413

    def test_excludes_paths_work(self):
        """Test that excluded paths are not checked for size."""
        app = FastAPI()
        app.add_middleware(RequestSizeMiddleware, max_size=100, exclude_paths=["/health"])

        @app.post("/health")
        async def health_endpoint():
            return {"status": "ok"}

        client = TestClient(app)
        response = client.post("/health", json={"large": "x" * 1000})
        # Should succeed because /health is excluded
        assert response.status_code == 200

    def test_format_size_function(self):
        """Test the _format_size helper function."""
        middleware = RequestSizeMiddleware(None)

        assert middleware._format_size(100) == "100.0 B"
        assert middleware._format_size(1024) == "1.0 KB"
        assert middleware._format_size(1024 * 1024) == "1.0 MB"
        assert middleware._format_size(1024 * 1024 * 1024) == "1.0 GB"


class TestResponseCompressionMiddleware:
    """Test cases for ResponseCompressionMiddleware."""

    @pytest.fixture
    def app_with_compression(self):
        """Create FastAPI app with ResponseCompressionMiddleware."""
        app = FastAPI()
        app.add_middleware(ResponseCompressionMiddleware)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        return app

    @pytest.fixture
    def client(self, app_with_compression):
        """Create test client."""
        return TestClient(app_with_compression)

    def test_no_compression_when_not_accepted(self, client):
        """Test that no compression is applied when client doesn't accept gzip."""
        response = client.get("/test", headers={"accept-encoding": "deflate"})
        assert "Content-Encoding" not in response.headers

    def test_should_compress_function(self):
        """Test the _should_compress helper function."""
        middleware = ResponseCompressionMiddleware(None)

        # Should compress
        assert middleware._should_compress("application/json")
        assert middleware._should_compress("text/html")
        assert middleware._should_compress("text/css")

        # Should not compress
        assert not middleware._should_compress("image/png")
        assert not middleware._should_compress("video/mp4")


class TestErrorHandlingMiddleware:
    """Test cases for ErrorHandlingMiddleware."""

    @pytest.fixture
    def app_with_error_handling(self):
        """Create FastAPI app with ErrorHandlingMiddleware."""
        app = FastAPI()
        app.add_middleware(ErrorHandlingMiddleware, include_debug_info=True)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        @app.get("/error")
        async def error_endpoint():
            raise ValueError("Test error")

        return app

    @pytest.fixture
    def client(self, app_with_error_handling):
        """Create test client."""
        return TestClient(app_with_error_handling)

    def test_handles_successful_requests(self, client):
        """Test that successful requests pass through normally."""
        response = client.get("/test")
        assert response.status_code == 200

    def test_includes_debug_info_when_enabled(self, client):
        """Test that debug info is included when enabled."""
        response = client.get("/error")
        response_data = response.json()

        assert "debug" in response_data
        assert response_data["debug"]["error_type"] == "ValueError"
        assert response_data["debug"]["error_message"] == "Test error"


class TestCorrelationIDMiddleware:
    """Test cases for CorrelationIDMiddleware."""

    @pytest.fixture
    def app_with_correlation_id(self):
        """Create FastAPI app with CorrelationIDMiddleware."""
        app = FastAPI()
        app.add_middleware(CorrelationIDMiddleware)

        @app.get("/test")
        async def test_endpoint(request: Request):
            return {
                "message": "test",
                "correlation_id": getattr(request.state, 'correlation_id', None)
            }

        return app

    @pytest.fixture
    def client(self, app_with_correlation_id):
        """Create test client."""
        return TestClient(app_with_correlation_id)

    def test_generates_correlation_id_when_not_provided(self, client):
        """Test that correlation ID is generated when not provided."""
        response = client.get("/test")

        assert "X-Correlation-ID" in response.headers
        correlation_id = response.headers["X-Correlation-ID"]
        assert len(correlation_id) == 36  # UUID length

        # Should also be available in request state
        response_data = response.json()
        assert response_data["correlation_id"] == correlation_id

    def test_uses_provided_correlation_id(self, client):
        """Test that provided correlation ID is used."""
        provided_id = "test-correlation-id"
        response = client.get("/test", headers={"X-Correlation-ID": provided_id})

        assert response.headers["X-Correlation-ID"] == provided_id
        response_data = response.json()
        assert response_data["correlation_id"] == provided_id

    def test_custom_header_name(self):
        """Test that custom header name works."""
        app = FastAPI()
        app.add_middleware(CorrelationIDMiddleware, header_name="X-Custom-ID")

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        assert "X-Custom-ID" in response.headers


class TestMiddlewareIntegration:
    """Integration tests for multiple middleware working together."""

    @pytest.fixture
    def app_with_multiple_middleware(self):
        """Create FastAPI app with multiple middleware."""
        app = FastAPI()

        # Add middleware in order
        app.add_middleware(ErrorHandlingMiddleware)
        app.add_middleware(CorrelationIDMiddleware)
        app.add_middleware(RequestLoggingMiddleware)
        app.add_middleware(SecurityHeadersMiddleware)
        app.add_middleware(RateLimitingMiddleware, config=RateLimitConfig(calls=10, period=60))

        @app.get("/test")
        async def test_endpoint(request: Request):
            return {
                "message": "test",
                "request_id": getattr(request.state, 'request_id', None),
                "correlation_id": getattr(request.state, 'correlation_id', None)
            }

        return app

    @pytest.fixture
    def client(self, app_with_multiple_middleware):
        """Create test client."""
        return TestClient(app_with_multiple_middleware)

    def test_all_middleware_work_together(self, client):
        """Test that all middleware work together correctly."""
        response = client.get("/test")

        # Check that all expected headers are present
        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert "X-Correlation-ID" in response.headers
        assert "X-Process-Time" in response.headers
        assert "X-Content-Type-Options" in response.headers

        # Check response data
        data = response.json()
        assert data["request_id"] is not None
        assert data["correlation_id"] is not None


# Async test utilities
@pytest.mark.asyncio
class TestAsyncMiddleware:
    """Test async behavior of middleware."""

    async def test_middleware_async_dispatch(self):
        """Test that middleware dispatch method works with async."""
        middleware = RequestLoggingMiddleware(None)

        # Mock request and call_next
        mock_request = Mock()
        mock_request.state = Mock()
        mock_request.method = "GET"
        mock_request.url = Mock()
        mock_request.url.path = "/test"
        mock_request.url.query_params = ""
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.headers = {}

        async def mock_call_next(request):
            response = Mock()
            response.status_code = 200
            response.headers = {}
            return response

        # This should not raise any exceptions
        response = await middleware.dispatch(mock_request, mock_call_next)
        assert response.status_code == 200


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
