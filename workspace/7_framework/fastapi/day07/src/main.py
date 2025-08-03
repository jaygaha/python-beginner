from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import time
import json
import os
from contextlib import asynccontextmanager
import logging

from middleware import (
    RequestLoggingMiddleware,
    SecurityHeadersMiddleware,
    RateLimitingMiddleware,
    RequestSizeMiddleware,
    ErrorHandlingMiddleware,
    CorrelationIDMiddleware,
    RateLimitConfig,
    get_cors_origins,
    get_trusted_hosts
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response validation
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Item name")
    price: float = Field(..., gt=0, description="Item price (must be positive)")


class ItemCreate(ItemBase):
    description: Optional[str] = Field(None, max_length=500, description="Item description")


class ItemResponse(ItemBase):
    id: int = Field(..., description="Item ID")
    created_at: float = Field(..., description="Creation timestamp")
    description: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: float
    request_id: Optional[str] = None
    middleware_active: bool = True
    version: str


class ErrorResponse(BaseModel):
    error: str
    message: str
    request_id: Optional[str] = None


# Application configuration
class AppConfig:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.debug = self.environment == "development"
        self.max_request_size = int(os.getenv("MAX_REQUEST_SIZE", 2 * 1024 * 1024))  # 2MB
        self.rate_limit_calls = int(os.getenv("RATE_LIMIT_CALLS", 50))
        self.rate_limit_period = int(os.getenv("RATE_LIMIT_PERIOD", 60))


config = AppConfig()


# Application lifecycle management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("Application starting up...")
    # Startup logic here (database connections, etc.)

    yield

    logger.info("Application shutting down...")
    # Cleanup logic here


# Create FastAPI application
app = FastAPI(
    title="Enhanced Middleware Demo API",
    version="2.0.0",
    description="API demonstrating enhanced middleware implementations with proper error handling and monitoring",
    lifespan=lifespan
)


# Add middleware in correct order (last added = first executed)
# Error handling should be outermost
app.add_middleware(ErrorHandlingMiddleware, include_debug_info=config.debug)

# Logging and correlation
app.add_middleware(CorrelationIDMiddleware)
app.add_middleware(RequestLoggingMiddleware, log_body=config.debug)

# Security
app.add_middleware(SecurityHeadersMiddleware)

# Rate limiting
rate_limit_config = RateLimitConfig(
    calls=config.rate_limit_calls,
    period=config.rate_limit_period
)
app.add_middleware(RateLimitingMiddleware, config=rate_limit_config)

# Request size limiting
app.add_middleware(
    RequestSizeMiddleware,
    max_size=config.max_request_size,
    exclude_paths=["/health", "/metrics"]  # Exclude monitoring endpoints
)

# Built-in compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time", "X-Correlation-ID"]
)

# Trusted host middleware (for production)
if not config.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=get_trusted_hosts()
    )


# In-memory database (replace with actual database in production)
class ItemDatabase:
    def __init__(self):
        self.items: List[Dict[str, Any]] = [
            {"id": 1, "name": "Item 1", "price": 10.0, "created_at": time.time(), "description": "First item"},
            {"id": 2, "name": "Item 2", "price": 20.0, "created_at": time.time(), "description": "Second item"},
            {"id": 3, "name": "Item 3", "price": 15.0, "created_at": time.time(), "description": "Third item"},
        ]
        self._next_id = 4

    def get_all(self) -> List[Dict[str, Any]]:
        return self.items.copy()

    def get_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        return next((item for item in self.items if item["id"] == item_id), None)

    def create(self, item_data: ItemCreate) -> Dict[str, Any]:
        new_item = {
            "id": self._next_id,
            "name": item_data.name,
            "price": item_data.price,
            "description": item_data.description,
            "created_at": time.time()
        }
        self.items.append(new_item)
        self._next_id += 1
        return new_item

    def update(self, item_id: int, item_data: ItemCreate) -> Optional[Dict[str, Any]]:
        item = self.get_by_id(item_id)
        if item:
            item.update({
                "name": item_data.name,
                "price": item_data.price,
                "description": item_data.description
            })
        return item

    def delete(self, item_id: int) -> bool:
        item = self.get_by_id(item_id)
        if item:
            self.items.remove(item)
            return True
        return False


# Database instance
db = ItemDatabase()


# Dependency functions
def get_request_info(request: Request) -> Dict[str, Any]:
    """Extract request information for responses."""
    return {
        "request_id": getattr(request.state, 'request_id', None),
        "correlation_id": getattr(request.state, 'correlation_id', None),
        "timestamp": time.time()
    }


# API Endpoints
@app.get(
    "/",
    summary="Root endpoint",
    description="Welcome endpoint with request information"
)
def read_root(request: Request) -> Dict[str, Any]:
    """Root endpoint returning welcome message and request info."""
    return {
        "message": "Welcome to Enhanced Middleware Demo API",
        "version": "2.0.0",
        "environment": config.environment,
        **get_request_info(request)
    }


@app.get(
    "/items/",
    response_model=Dict[str, Any],
    summary="Get all items",
    description="Retrieve all items from the database"
)
def get_items(request: Request) -> Dict[str, Any]:
    """Get all items with simulated processing delay."""
    # Simulate some processing time
    time.sleep(0.1)

    return {
        "items": [ItemResponse(**item) for item in db.get_all()],
        "count": len(db.items),
        **get_request_info(request)
    }


@app.get(
    "/items/{item_id}",
    response_model=Dict[str, Any],
    responses={404: {"model": ErrorResponse}},
    summary="Get item by ID",
    description="Retrieve a specific item by its ID"
)
def get_item(item_id: int, request: Request) -> Dict[str, Any]:
    """Get a specific item by ID."""
    item = db.get_by_id(item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID {item_id} not found"
        )

    return {
        "item": ItemResponse(**item),
        **get_request_info(request)
    }


@app.post(
    "/items/",
    response_model=Dict[str, Any],
    status_code=201,
    summary="Create new item",
    description="Create a new item in the database"
)
def create_item(item_data: ItemCreate, request: Request) -> Dict[str, Any]:
    """Create a new item."""
    new_item = db.create(item_data)

    logger.info(f"Created new item: {new_item['id']}")

    return {
        "item": ItemResponse(**new_item),
        "message": "Item created successfully",
        **get_request_info(request)
    }


@app.put(
    "/items/{item_id}",
    response_model=Dict[str, Any],
    responses={404: {"model": ErrorResponse}},
    summary="Update item",
    description="Update an existing item"
)
def update_item(item_id: int, item_data: ItemCreate, request: Request) -> Dict[str, Any]:
    """Update an existing item."""
    updated_item = db.update(item_id, item_data)
    if not updated_item:
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID {item_id} not found"
        )

    logger.info(f"Updated item: {item_id}")

    return {
        "item": ItemResponse(**updated_item),
        "message": "Item updated successfully",
        **get_request_info(request)
    }


@app.delete(
    "/items/{item_id}",
    responses={404: {"model": ErrorResponse}},
    summary="Delete item",
    description="Delete an item from the database"
)
def delete_item(item_id: int, request: Request) -> Dict[str, Any]:
    """Delete an item."""
    if not db.delete(item_id):
        raise HTTPException(
            status_code=404,
            detail=f"Item with ID {item_id} not found"
        )

    logger.info(f"Deleted item: {item_id}")

    return {
        "message": f"Item {item_id} deleted successfully",
        **get_request_info(request)
    }


@app.get(
    "/large-data",
    summary="Get large dataset",
    description="Generate large response to test compression middleware"
)
def get_large_data(request: Request, size: int = 1000) -> Dict[str, Any]:
    """Generate large response to test compression."""
    if size > 10000:  # Prevent abuse
        raise HTTPException(status_code=400, detail="Size too large (max: 10000)")

    large_data = {
        "data": [f"item_{i}" for i in range(size)],
        "metadata": {
            "count": size,
            "size_mb": round(size * 10 / 1024 / 1024, 2),  # Rough estimate
            **get_request_info(request)
        }
    }
    return large_data


@app.post(
    "/large-upload",
    summary="Handle large upload",
    description="Test endpoint for request size middleware"
)
def handle_large_upload(data: Dict[str, Any], request: Request) -> Dict[str, Any]:
    """Handle large upload - protected by RequestSizeMiddleware."""
    data_size = len(json.dumps(data))

    return {
        "message": "Upload successful",
        "data_size_bytes": data_size,
        "data_size_kb": round(data_size / 1024, 2),
        **get_request_info(request)
    }


@app.get(
    "/slow-endpoint",
    summary="Slow processing endpoint",
    description="Simulate slow processing for testing"
)
def slow_endpoint(request: Request, delay: float = 2.0) -> Dict[str, Any]:
    """Simulate slow processing."""
    if delay > 10:  # Prevent abuse
        raise HTTPException(status_code=400, detail="Delay too long (max: 10s)")

    time.sleep(delay)
    return {
        "message": f"Processed after {delay}s delay",
        **get_request_info(request)
    }


@app.get(
    "/error-test",
    summary="Error testing endpoint",
    description="Trigger an error to test error handling middleware"
)
def error_test() -> None:
    """Trigger an error to test error handling middleware."""
    raise Exception("This is a test error for middleware testing")


@app.get(
    "/rate-limit-test",
    summary="Rate limit testing",
    description="Test endpoint for rate limiting middleware (use repeatedly to trigger limit)"
)
def rate_limit_test(request: Request) -> Dict[str, Any]:
    """Test rate limiting."""
    return {
        "message": "Rate limit test successful",
        "info": f"Limit: {config.rate_limit_calls} requests per {config.rate_limit_period} seconds",
        **get_request_info(request)
    }


@app.options(
    "/cors-preflight",
    summary="CORS preflight test",
    description="Test CORS preflight handling"
)
def cors_preflight() -> Dict[str, str]:
    """Handle CORS preflight requests."""
    return {"message": "CORS preflight successful"}


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Application health check endpoint",
    tags=["monitoring"]
)
def health_check(request: Request) -> HealthResponse:
    """Health check endpoint for monitoring."""
    return HealthResponse(
        status="healthy",
        timestamp=time.time(),
        request_id=getattr(request.state, 'request_id', None),
        middleware_active=True,
        version="2.0.0"
    )


@app.get(
    "/metrics",
    summary="Basic metrics",
    description="Basic application metrics",
    tags=["monitoring"]
)
def get_metrics(request: Request) -> Dict[str, Any]:
    """Basic metrics endpoint."""
    return {
        "items_count": len(db.items),
        "environment": config.environment,
        "uptime_check": "healthy",
        **get_request_info(request)
    }


# Exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            **get_request_info(request)
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=config.debug,
        log_level="info" if not config.debug else "debug"
    )
