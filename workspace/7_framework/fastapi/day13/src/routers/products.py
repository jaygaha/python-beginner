from fastapi import APIRouter, Query, status
from typing import List, Optional
from src.models.schemas import (
    ProductCreate, ProductResponse
)

router = APIRouter(prefix="/api/v1/products", tags=["products"])

# Mock database
fake_products_db = [
    {
        "id": 1,
        "name": "Wireless Headphones",
        "description": "High-quality wireless headphones with noise cancellation",
        "price": 99.99,
        "category": "Electronics",
        "stock_quantity": 50,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None
    },
    {
        "id": 2,
        "name": "Smartphone Case",
        "description": "Protective case for smartphones",
        "price": 19.99,
        "category": "Accessories",
        "stock_quantity": 100,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": None
    }
]


@router.get(
    "/",
    response_model=List[ProductResponse],
    summary="Get all products",
    description="Retrieve a paginated list of products with optional filtering.",
    responses={
        200: {
            "description": "List of products",
            "content": {
                "application/json": {
                    "examples": {
                        "multiple_products": {
                            "summary": "Multiple products",
                            "value": [
                                {
                                    "id": 1,
                                    "name": "Wireless Headphones",
                                    "description": "High-quality wireless headphones",
                                    "price": 99.99,
                                    "category": "Electronics",
                                    "stock_quantity": 50,
                                    "created_at": "2023-01-01T00:00:00",
                                    "updated_at": None
                                }
                            ]
                        },
                        "empty_list": {
                            "summary": "No products found",
                            "value": []
                        }
                    }
                }
            }
        }
    }
)
async def get_products(
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of products to return"),
    category: Optional[str] = Query(None, description="Filter by product category"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter")
):
    """Get products with optional filtering and pagination."""
    products = fake_products_db.copy()

    if category:
        products = [p for p in products if p["category"].lower() == category.lower()]
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    return products[skip:skip + limit]


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    description="Add a new product to the catalog.",
    responses={
        201: {"description": "Product created successfully"}
    }
)
async def create_product(product: ProductCreate):
    """Create a new product in the catalog."""
    new_product = {
        "id": len(fake_products_db) + 1,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "category": product.category,
        "stock_quantity": product.stock_quantity,
        "created_at": "2023-11-01T10:30:00",
        "updated_at": None
    }
    fake_products_db.append(new_product)
    return new_product
