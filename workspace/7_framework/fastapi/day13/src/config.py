from pydantic_settings import BaseSettings
from typing import Dict, Any


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


settings = Settings()
