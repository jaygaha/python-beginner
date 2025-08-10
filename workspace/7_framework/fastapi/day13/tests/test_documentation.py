import pytest
# from httpx import WSGITransport, ASGITransport
# from starlette.middleware.wsgi import WSGITransport
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app=app)
# client = TestClient(transport=WSGITransport(app=app))
# client = TestClient(app, transport=ASGITransport(app=app))
# client = TestClient(transport=WSGITransport(app=app))


class TestOpenAPIDocumentation:
    """Test OpenAPI documentation generation and customization"""

    def test_openapi_schema_generation(self):
        """Test that OpenAPI schema is generated correctly"""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert schema["info"]["title"] == "FastAPI E-commerce API"
        assert schema["info"]["version"] == "2.1.0"
        assert "description" in schema["info"]
        assert schema["info"]["contact"]["name"] == "API Support Team"
        assert schema["info"]["license"]["name"] == "MIT License"

    def test_custom_servers_in_schema(self):
        """Test that custom servers are included in OpenAPI schema"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        assert "servers" in schema
        servers = schema["servers"]
        assert len(servers) == 3

        server_urls = [server["url"] for server in servers]
        assert "https://api.ecommerce.com" in server_urls
        assert "https://staging-api.ecommerce.com" in server_urls
        assert "http://localhost:8000" in server_urls

    def test_security_schemes_in_schema(self):
        """Test that security schemes are properly defined"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        assert "components" in schema
        assert "securitySchemes" in schema["components"]

        security_schemes = schema["components"]["securitySchemes"]
        assert "bearerAuth" in security_schemes
        assert "apiKey" in security_schemes

        # Test bearer auth configuration
        bearer_auth = security_schemes["bearerAuth"]
        assert bearer_auth["type"] == "http"
        assert bearer_auth["scheme"] == "bearer"
        assert bearer_auth["bearerFormat"] == "JWT"

    def test_tags_metadata(self):
        """Test that tags metadata is properly configured"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        # Tags might be in the schema or derived from router tags
        if "tags" in schema:
            tags = {tag["name"]: tag for tag in schema["tags"]}

            assert "users" in tags
            assert "products" in tags
            assert "orders" in tags
            assert "admin" in tags

            # Test external docs for users if present
            if "users" in tags and "externalDocs" in tags["users"]:
                users_tag = tags["users"]
                assert users_tag["externalDocs"]["url"] == "https://docs.ecommerce-api.com/users"
        else:
            # If tags aren't in the main schema, check if they exist in the paths
            paths = schema.get("paths", {})
            all_tags = set()
            for path_data in paths.values():
                for method_data in path_data.values():
                    if isinstance(method_data, dict) and "tags" in method_data:
                        all_tags.update(method_data["tags"])

            assert "users" in all_tags
            assert "products" in all_tags
            assert "orders" in all_tags
            assert "admin" in all_tags

    def test_endpoint_documentation_structure(self):
        """Test that endpoints have proper documentation structure"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        # Test users endpoint documentation
        users_get = schema["paths"]["/api/v1/users/"]["get"]
        assert "summary" in users_get
        assert "description" in users_get
        assert "responses" in users_get
        assert "parameters" in users_get

        # Test that custom headers are added
        headers = [param for param in users_get["parameters"] if param.get("in") == "header"]
        request_id_header = next(
            (h for h in headers if h.get("name") == "X-Request-ID"), None
        )
        assert request_id_header is not None

    def test_response_examples(self):
        """Test that response examples are properly configured"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        # Test products endpoint response examples
        products_get = schema["paths"]["/api/v1/products/"]["get"]
        responses = products_get["responses"]

        assert "200" in responses
        response_200 = responses["200"]
        assert "content" in response_200
        assert "application/json" in response_200["content"]

        json_content = response_200["content"]["application/json"]
        if "examples" in json_content:
            examples = json_content["examples"]
            assert "multiple_products" in examples or "empty_list" in examples


class TestCustomDocumentationPages:
    """Test custom documentation pages and UI"""

    def test_custom_swagger_ui_accessible(self):
        """Test that custom Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Check that the response contains Swagger UI elements
        content = response.text
        assert "swagger-ui" in content.lower()
        assert "FastAPI E-commerce API" in content

    def test_custom_redoc_accessible(self):
        """Test that custom ReDoc is accessible"""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

        # Check that the response contains ReDoc elements
        content = response.text
        assert "redoc" in content.lower()
        assert "FastAPI E-commerce API" in content

    def test_oauth2_redirect_endpoint(self):
        """Test OAuth2 redirect endpoint for Swagger UI"""
        response = client.get("/docs/oauth2-redirect")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]


class TestAPIVersioningAndDeprecation:
    """Test API versioning and deprecation features"""

    def test_api_info_endpoint(self):
        """Test API information endpoint"""
        response = client.get("/api/v1/info")
        assert response.status_code == 200

        data = response.json()
        assert data["api_version"] == "v1"
        assert "app_version" in data
        assert "features" in data
        assert data["deprecated"] is False

    def test_deprecated_endpoint_marked(self):
        """Test that deprecated endpoints are properly marked"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        # Find deprecated endpoint in schema
        legacy_endpoint = schema["paths"]["/api/v1/legacy-endpoint"]["get"]
        assert legacy_endpoint["deprecated"] is True
        assert "This endpoint is deprecated and will be removed in v2.0" in legacy_endpoint["description"]

    def test_deprecated_endpoint_still_works(self):
        """Test that deprecated endpoint still functions"""
        response = client.get("/api/v1/legacy-endpoint")
        assert response.status_code == 200

        data = response.json()
        assert "deprecated" in data["message"].lower()


class TestErrorDocumentation:
    """Test error response documentation"""

    def test_error_responses_documented(self):
        """Test that error responses are properly documented"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        # Test user by ID endpoint error documentation
        user_by_id = schema["paths"]["/api/v1/users/{user_id}"]["get"]
        responses = user_by_id["responses"]

        assert "404" in responses
        error_404 = responses["404"]
        assert "description" in error_404
        assert error_404["description"] == "User not found"

        # Check if error model is referenced
        if "content" in error_404:
            json_content = error_404["content"]["application/json"]
            assert "example" in json_content

    def test_validation_error_documentation(self):
        """Test that validation errors are documented"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        # Test create user endpoint validation documentation
        create_user = schema["paths"]["/api/v1/users/"]["post"]
        responses = create_user["responses"]

        assert "422" in responses
        validation_error = responses["422"]
        assert "Validation error" in validation_error["description"]


class TestHealthAndMonitoring:
    """Test health check and monitoring endpoints"""

    def test_health_check_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data

    def test_health_check_documented(self):
        """Test that health check is properly documented"""
        response = client.get("/api/v1/openapi.json")
        schema = response.json()

        health_endpoint = schema["paths"]["/health"]["get"]
        assert "admin" in health_endpoint["tags"]
        assert "Health check" in health_endpoint["summary"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
