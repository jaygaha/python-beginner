from fastapi import APIRouter, HTTPException, Path, status
from src.models.schemas import OrderCreate, OrderResponse, ErrorResponse

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])

# Mock databases
fake_orders_db = []
fake_products_db = [
    {"id": 1, "name": "Wireless Headphones", "price": 99.99, "stock_quantity": 50},
    {"id": 2, "name": "Smartphone Case", "price": 19.99, "stock_quantity": 100}
]


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
    description="Place a new order with multiple items.",
    responses={
        201: {
            "description": "Order created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "user_id": 1,
                        "items": [
                            {
                                "product_id": 1,
                                "product_name": "Wireless Headphones",
                                "quantity": 1,
                                "unit_price": 99.99,
                                "total_price": 99.99
                            }
                        ],
                        "total_amount": 99.99,
                        "status": "pending",
                        "shipping_address": "123 Main St, City, State 12345",
                        "created_at": "2023-11-01T10:30:00",
                        "updated_at": None
                    }
                }
            }
        },
        400: {
            "description": "Invalid order data",
            "model": ErrorResponse
        }
    }
)
async def create_order(order: OrderCreate):
    """
    Create a new order.

    This endpoint allows customers to place orders with multiple items.
    The system will validate product availability and calculate totals automatically.
    """
    # Validate products and calculate total
    order_items = []
    total_amount = 0.0

    for item in order.items:
        product = next((p for p in fake_products_db if p["id"] == item.product_id), None)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with ID {item.product_id} not found"
            )

        if product["stock_quantity"] < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product['name']}"
            )

        item_total = product["price"] * item.quantity
        total_amount += item_total

        order_items.append({
            "product_id": item.product_id,
            "product_name": product["name"],
            "quantity": item.quantity,
            "unit_price": product["price"],
            "total_price": item_total
        })

    new_order = {
        "id": len(fake_orders_db) + 1,
        "user_id": 1,  # Mock user ID
        "items": order_items,
        "total_amount": total_amount,
        "status": "pending",
        "shipping_address": order.shipping_address,
        "created_at": "2023-11-01T10:30:00",
        "updated_at": None
    }

    fake_orders_db.append(new_order)
    return new_order


@router.get(
    "/{order_id}",
    response_model=OrderResponse,
    summary="Get order by ID",
    description="Retrieve detailed information about a specific order.",
    responses={
        200: {"description": "Order found successfully"},
        404: {"description": "Order not found", "model": ErrorResponse}
    }
)
async def get_order(
    order_id: int = Path(..., gt=0, description="The unique identifier of the order")
):
    """Get detailed information about a specific order."""
    order = next((order for order in fake_orders_db if order["id"] == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    return order
