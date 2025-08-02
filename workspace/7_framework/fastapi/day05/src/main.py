from fastapi import FastAPI, HTTPException, status, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from exceptions import DuplicateItemError, InsufficientStockError, ItemNotFoundError, UnauthorizedError, ForbiddenError
from models.stock import Item, Order, OrderStatus
from typing import List, Dict, Any
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="FastAPI E-Commerce API", version="1.0.0", description="An API for managing an e-commerce platform", docs_url="/api/docs")

# Mock db
# In-memory database - a simple list to store our required records.
items_db: List[Dict[str, Any]] = []
orders_db: List[Dict[str, Any]] = []
next_item_id = 1
next_order_id = 1


# Custom exception handlers
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    logger.error(f"Item not found: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Item Not Found",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(InsufficientStockError)
async def insufficient_stock_handler(request: Request, exc: InsufficientStockError):
    logger.error(f"Insufficient stock: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Insufficient Stock",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(DuplicateItemError)
async def duplicate_item_handler(request: Request, exc: DuplicateItemError):
    logger.error(f"Duplicate item: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Duplicate Item",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )


@app.exception_handler(UnauthorizedError)
async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
    logger.error(f"Unauthorized error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error": "Unauthorized",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(ForbiddenError)
async def forbidden_error_handler(request: Request, exc: ForbiddenError):
    logger.error(f"Forbidden error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error": "Forbidden",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"HTTP exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )


# Routes
# Item endpoints
@app.post("/items/", response_model=Item, status_code=status.HTTP_201_CREATED, summary="Create an item", tags=["Items"])
async def create_item(item: Item):
    global next_item_id

    # Check for duplicate SKU
    existing_item = next((i for i in items_db if i["sku"] == item.sku), None)

    if existing_item:
        raise DuplicateItemError("sku", item.sku)

    item_dict = item.model_dump()
    item_dict["id"] = next_item_id
    items_db.append(item_dict)
    next_item_id += 1

    logger.info(f"Created item with id {item_dict['id']}")
    return item_dict

@app.get("/items/{item_id}", response_model=Item, summary="Get an item by ID", tags=["Items"])
async def get_item(item_id: int):
    item = next((i for i in items_db if i["id"] == item_id), None)

    if not item:
        raise ItemNotFoundError(item_id)

    logger.info(f"Retrieved item with id {item_id}")
    return item

@app.get("/items/", response_model=List[Item], summary="Get all items", tags=["Items"])
async def get_items():
    logger.info("Retrieved all items")
    return items_db

@app.put("/items/{item_id}", response_model=Item, summary="Update an item by ID", tags=["Items"])
async def update_item(item_id: int, item_update: Item):
    item_index = next((i for i, item in enumerate(items_db) if item["id"] == item_id), None)

    if item_index is None:
        raise ItemNotFoundError(item_id)

    # Check for duplicate SKU (excluding current item)
    existing_item = next((i for i in items_db if i["sku"] == item_update.sku and i["id"] != item_id), None)
    if existing_item:
        raise DuplicateItemError("sku", item_update.sku)

    item_dict = item_update.model_dump()
    item_dict["id"] = item_id
    items_db[item_index] = item_dict

    logger.info(f"Updated item with id {item_id}")
    return item_dict

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete an item by ID", tags=["Items"])
async def delete_item(item_id: int):
    item_index = next((i for i, item in enumerate(items_db) if item["id"] == item_id), None)

    if item_index is None:
        raise ItemNotFoundError(item_id)

    del items_db[item_index]
    logger.info(f"Deleted item with id {item_id}")

# Order endpoints
@app.post("/orders/", response_model=Order, status_code=status.HTTP_201_CREATED, summary="Create an order", tags=["Orders"])
async def create_order(order: Order):
    global next_order_id

    # Validate item exists and sufficient stock
    total_amount = 0.0
    for order_item in order.items:
        item = next((item for item in items_db if item["id"] == order_item.item_id), None)

        if not item:
            raise ItemNotFoundError(order_item.item_id)

        if item["stock"] < order_item.quantity:
            raise InsufficientStockError(order_item.item_id, order_item.quantity, item["stock"])

        total_amount += item["price"] * order_item.quantity

    # Update stock
    for order_item in order.items:
        item = next(item for item in items_db if item["id"] == order_item.item_id)
        item["stock"] -= order_item.quantity

    order_dict = order.model_dump()
    order_dict.update({
        "id": next_order_id,
        "customer_email": order.customer_email,
        "total_amount": total_amount,
        "created_at": datetime.now(),
        "status": OrderStatus.pending
    })
    orders_db.append(order_dict)
    next_order_id += 1

    logger.info(f"Created order with id {order_dict['id']}")
    return order_dict

@app.get("/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    order = next((order for order in orders_db if order["id"] == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )
    return order

@app.patch("/orders/{order_id}/status", response_model=Order)
def update_order_status(order_id: int, new_status: OrderStatus):
    order = next((order for order in orders_db if order["id"] == order_id), None)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with id {order_id} not found"
        )

    # Business logic for status transitions
    current_status = OrderStatus(order["status"])

    # Define valid transitions
    valid_transitions = {
        OrderStatus.pending: [OrderStatus.processing, OrderStatus.cancelled],
        OrderStatus.processing: [OrderStatus.shipped, OrderStatus.cancelled],
        OrderStatus.shipped: [OrderStatus.delivered],
        OrderStatus.delivered: [],
        OrderStatus.cancelled: []
    }

    if new_status not in valid_transitions[current_status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot transition from {current_status} to {new_status}"
        )

    order["status"] = new_status

    logger.info(f"Updated order with id {order_id} status to {new_status}")
    return order

# Health check endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "items_count": len(items_db),
        "orders_count": len(orders_db)
    }
