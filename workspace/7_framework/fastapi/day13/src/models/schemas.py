from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"
    MODERATOR = "moderator"


class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


# User Schemas
class UserBase(BaseModel):
    """Base user model with common attributes"""
    email: EmailStr = Field(..., json_schema_extra={"description": "User's email address", "example": "john.doe@example.com"})
    first_name: str = Field(..., json_schema_extra={"min_length": 1, "max_length": 50, "description": "User's first name", "example": "John"})
    last_name: str = Field(..., json_schema_extra={"min_length": 1, "max_length": 50, "description": "User's last name", "example": "Doe"})
    role: UserRole = Field(default=UserRole.CUSTOMER, description="User's role in the system")


class UserCreate(UserBase):
    """Schema for creating a new user"""
    password: str = Field(...,json_schema_extra={"min_length": 8,"description": "User's password (minimum 8 characters)", "example": "SecurePass123!"})

    @field_validator('password')
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserResponse(UserBase):
    """Schema for user response (excludes password)"""
    id: int = Field(..., json_schema_extra={"description": "Unique user identifier", "example": 1})
    is_active: bool = Field(default=True, description="Whether the user account is active")
    created_at: datetime = Field(..., description="Account creation timestamp")

    class ConfigDict:
        from_attributes = True


class UserUpdate(BaseModel):
    """Schema for updating user information"""
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None


# Product Schemas
class ProductBase(BaseModel):
    """Base product model"""
    name: str = Field(..., json_schema_extra={"min_length": 1, "max_length": 200, "description": "Product name", "example": "Wireless Headphones"})
    description: Optional[str] = Field(None, max_length=1000, description="Product description")
    price: float = Field(..., json_schema_extra={"gt": 0, "description": "Product price in USD", "example": 99.99})
    category: str = Field(..., json_schema_extra={"description": "Product category", "example": "Electronics"})
    stock_quantity: int = Field(..., json_schema_extra={"ge": 0, "description": "Available stock quantity", "example":50})


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int = Field(..., json_schema_extra={"description": "Unique product identifier", "example": 1})
    created_at: datetime = Field(..., description="Product creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class ConfigDict:
        from_attributes = True


class ProductUpdate(BaseModel):
    """Schema for updating product information"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)


# Order Schemas
class OrderItemCreate(BaseModel):
    """Schema for creating an order item"""
    product_id: int = Field(..., json_schema_extra={"description": "Product identifier", "example": 1})
    quantity: int = Field(..., json_schema_extra={"gt": 0, "description": "Quantity to order", "example": 2})


class OrderItemResponse(BaseModel):
    """Schema for order item response"""
    product_id: int = Field(..., description="Product identifier")
    product_name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Ordered quantity")
    unit_price: float = Field(..., description="Price per unit")
    total_price: float = Field(..., description="Total price for this item")


class OrderCreate(BaseModel):
    """Schema for creating a new order"""
    items: List[OrderItemCreate] = Field(..., min_length=1, description="List of items to order")
    shipping_address: str = Field(..., json_schema_extra={"min_length": 10, "description": "Shipping address", "example": "123 Main St, City, State 12345"})


class OrderResponse(BaseModel):
    """Schema for order response"""
    id: int = Field(..., json_schema_extra={"description": "Unique order identifier", "example": 1})
    user_id: int = Field(..., description="User who placed the order")
    items: List[OrderItemResponse] = Field(..., description="Ordered items")
    total_amount: float = Field(..., description="Total order amount")
    status: OrderStatus = Field(..., description="Current order status")
    shipping_address: str = Field(..., description="Shipping address")
    created_at: datetime = Field(..., description="Order creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class ConfigDict:
        from_attributes = True


# Error Schemas
class ErrorResponse(BaseModel):
    """Standard error response schema"""
    detail: str = Field(..., json_schema_extra={"description": "Error message", "example": "Resource not found"})
    error_code: Optional[str] = Field(None, json_schema_extra={"description": "Specific error code", "example": "USER_NOT_FOUND"})


class ValidationErrorResponse(BaseModel):
    """Validation error response schema"""
    detail: List[dict] = Field(..., description="List of validation errors")

    class ConfigDict:
        json_schema_extra = {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "email"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }
