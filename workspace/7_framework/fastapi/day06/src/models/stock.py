from enums.order_enum import OrderStatus
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class Item(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=2, max_length=100)
    price: float = Field(..., gt=0)
    is_active: bool = True
    owner_id: int

class OrderItem(BaseModel):
    id: Optional[int] = None
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class Order(BaseModel):
    id: Optional[int] = None
    items: List[OrderItem]
    customer_email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    status: OrderStatus = OrderStatus.pending
    total_amount: float = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('items')
    def items_must_not_be_empty(cls, value):
        if not value:
            raise ValueError('Order must have at least one item')
        return value

class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime
    path: Optional[str] = None
