# FastAPI Day 13: Advanced OpenAPI and Documentation

Welcome to **Day 13** of the FastAPI tutorial series! While FastAPI provides excellent out-of-the-box documentation, this tutorial focuses on elevating it to a professional standard. You'll learn how to customize the OpenAPI schema, add detailed metadata, and create a rich, user-friendly experience for your API consumers.

---

## What You'll Learn

-   **Custom OpenAPI Schema**: Override FastAPI's default OpenAPI generation to add custom server information, security schemes, and global parameters.
-   **Centralized Configuration**: Use `pydantic-settings` to manage all API metadata (like title, version, and contact info) in a single, clean configuration file.
-   **Rich Endpoint Documentation**: Enhance your endpoints with summaries, detailed descriptions, response examples, and clear error models.
-   **Custom Documentation UIs**: Serve customized versions of Swagger UI and ReDoc with enhanced display options.
-   **API Versioning & Deprecation**: Document API versions and clearly mark endpoints as deprecated to guide users through API evolution.
-   **Testing Documentation**: Write automated tests to ensure your documentation remains accurate and complete.

---

## Key Concepts

This project is a mock e-commerce API with advanced documentation features.

-   `src/main.py`: Contains the main FastAPI application, custom OpenAPI generation logic, and routes for custom documentation UIs.
-   `src/config.py`: Uses `pydantic-settings` to manage all documentation-related metadata.
-   `src/routers/`: API routers for users, products, and orders, with extensive documentation.
-   `src/models/schemas.py`: Pydantic models with detailed field descriptions and examples.
-   `tests/test_documentation.py`: `pytest` tests for validating the OpenAPI schema and custom documentation pages.

### 1. Centralized Metadata with `pydantic-settings`

To keep our main application file clean and manage metadata efficiently, we define everything in a `Settings` class. This includes the app's title, version, contact information, license, and tag metadata for grouping endpoints.

```python-beginner/workspace/7_framework/fastapi/day13/src/config.py#L5-L53
class Settings(BaseSettings):
    app_name: str = "FastAPI E-commerce API"
    app_version: str = "2.1.0"
    app_description: str = """
    A comprehensive e-commerce API built with FastAPI.

    ## Features

    * **Users**: Create, read, update, and delete user accounts
    * **Products**: Manage product catalog with categories and inventory
    * **Orders**: Handle order processing and tracking

    ## Authentication

    Some endpoints require authentication. Use the `/auth/login` endpoint to obtain a token.
    """

    contact_info: Dict[str, Any] = {
        "name": "API Support Team",
        "email": "support@ecommerce-api.com",
        "url": "https://ecommerce-api.com/support"
    }

    license_info: Dict[str, Any] = {
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }

    tags_metadata: list = [
        {
            "name": "users",
            "description": "User management operations. Create, read, update, and delete user accounts.",
            "externalDocs": {
                "description": "User Guide",
                "url": "https://docs.ecommerce-api.com/users"
            }
        },
        {
            "name": "products",
            "description": "Product catalog management. Handle inventory, categories, and pricing.",
            "externalDocs": {
                "description": "Product Management Guide",
                "url": "https://docs.ecommerce-api.com/products"
            }
        },
        {
            "name": "orders",
            "description": "Order processing and tracking. Handle customer purchases and fulfillment.",
        },
        {
            "name": "admin",
            "description": "Administrative operations. Requires admin privileges.",
        }
    ]
```

### 2. Customizing the OpenAPI Schema

We create a `custom_openapi` function to programmatically modify the schema. This allows us to add environment-specific server URLs (dev, staging, prod), define security schemes like JWT and API Keys, and inject global headers.

```python-beginner/workspace/7_framework/fastapi/day13/src/main.py#L14-L83
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
```

### 3. Detailed Endpoint Documentation

In each router, we use decorator parameters like `summary`, `description`, and a `responses` dictionary to provide rich context. This includes examples for successful responses and structured models for errors.

```python-beginner/workspace/7_framework/fastapi/day13/src/routers/users.py#L90-L132
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique identifier.",
    responses={
        200: {
            "description": "User found successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "role": "customer",
                        "is_active": True,
                        "created_at": "2023-01-01T00:00:00"
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found",
                        "error_code": "USER_NOT_FOUND"
                    }
                }
            }
        }
    }
)
async def get_user(
    user_id: int = Path(..., gt=0, description="The unique identifier of the user", examples=[1])
):
    """
    Get a specific user by ID.

    Returns detailed information about a user including their profile data and account status.
    """
    user = next((user for user in fake_users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
```

### 4. Testing Your Documentation

It's crucial to test your documentation just like your code. Using `TestClient`, we can fetch `/api/v1/openapi.json` and assert that our customizations—like the title, version, and server information—are present and correct.

```python-beginner/workspace/7_framework/fastapi/day13/tests/test_documentation.py#L15-L26
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
```

---

## Next Steps

-   Navigate to the `day13` directory: `cd day13`.
-   Install the dependencies: `pip install -r requirements.txt`.
-   Run the application: `uvicorn src.main:app --reload`.
-   Explore the enhanced documentation at `http://localhost:8000/docs` (Swagger) and `http://localhost:8000/redoc` (ReDoc).
-   Run the automated tests with `python -m pytest`.

---