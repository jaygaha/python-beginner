from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.openapi.utils import get_openapi

from src.config import settings
from src.routers import users, products, orders


def custom_openapi():
    """Generate custom OpenAPI schema with enhanced metadata"""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        routes=app.routes,
        contact=settings.contact_info,
        license_info=settings.license_info,
    )

    # Add custom server information
    openapi_schema["servers"] = [
        {
            "url": "https://api.ecommerce.com",
            "description": "Production server"
        },
        {
            "url": "https://staging-api.ecommerce.com",
            "description": "Staging server"
        },
        {
            "url": "http://localhost:8000",
            "description": "Development server"
        }
    ]

    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT token in the format: Bearer <token>"
        },
        "apiKey": {
            "type": "apiKey",
            "in": "header",
            "name": "X-API-Key",
            "description": "API key for authentication"
        }
    }

    # Add global security requirement
    openapi_schema["security"] = [
        {"bearerAuth": []},
        {"apiKey": []}
    ]

    # Enhance path descriptions
    for path, path_item in openapi_schema["paths"].items():
        for method, operation in path_item.items():
            if method in ["get", "post", "put", "delete", "patch"]:
                # Add custom headers to all operations
                if "parameters" not in operation:
                    operation["parameters"] = []

                operation["parameters"].extend([
                    {
                        "name": "X-Request-ID",
                        "in": "header",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "format": "uuid",
                            "description": "Unique request identifier for tracking"
                        }
                    }
                ])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


# Create FastAPI app with enhanced configuration
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
    contact=settings.contact_info,
    license_info=settings.license_info,
    openapi_tags=settings.tags_metadata,
    docs_url=None,  # Disable default docs
    redoc_url=None,  # Disable default redoc
    openapi_url="/api/v1/openapi.json"  # Custom OpenAPI URL
)

# Set custom OpenAPI schema
app.openapi = custom_openapi

# Include routers
app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    """Custom Swagger UI with enhanced styling"""
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css",
        swagger_ui_parameters={
            "deepLinking": True,
            "displayRequestDuration": True,
            "docExpansion": "none",
            "operationsSorter": "method",
            "filter": True,
            "showExtensions": True,
            "showCommonExtensions": True,
            "defaultModelsExpandDepth": 2,
            "defaultModelExpandDepth": 2,
            "displayOperationId": True,
        }
    )


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    """Custom ReDoc documentation"""
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=f"{app.title} - API Documentation",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
        with_google_fonts=True,
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    """OAuth2 redirect for Swagger UI"""
    return get_swagger_ui_oauth2_redirect_html()


# Health check endpoint
@app.get("/health", tags=["admin"], summary="Health check", description="Check API health status")
async def health_check():
    """
    Health check endpoint for monitoring.

    Returns the current status of the API and basic system information.
    """
    return {
        "status": "healthy",
        "version": settings.app_version,
        "timestamp": "2023-11-01T10:30:00Z"
    }


# API versioning example
@app.get("/api/v1/info", tags=["admin"], summary="API Information")
async def api_info():
    """Get information about the current API version."""
    return {
        "api_version": "v1",
        "app_version": settings.app_version,
        "features": ["users", "products", "orders"],
        "deprecated": False
    }


# Add a deprecated endpoint to show deprecation warnings
@app.get(
    "/api/v1/legacy-endpoint",
    tags=["admin"],
    summary="Legacy Endpoint (Deprecated)",
    description="This endpoint is deprecated and will be removed in v2.0",
    deprecated=True
)
async def legacy_endpoint():
    """
    ⚠️ **DEPRECATED**: This endpoint will be removed in API v2.0

    Please use the new endpoints instead.
    """
    return {"message": "This endpoint is deprecated"}
