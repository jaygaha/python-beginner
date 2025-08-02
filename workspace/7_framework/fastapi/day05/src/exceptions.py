"""
Global exceptions for the FastAPI application.
"""

from fastapi import HTTPException, status

class ItemNotFoundError(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )

class InsufficientStockError(HTTPException):
    def __init__(self, item_id: int, requested: int, available: int):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Insufficient stock for item {item_id}. Requested: {requested}, Available: {available}"
        )

class DuplicateItemError(HTTPException):
    def __init__(self, field: str, value: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Item with ID {field} '{value}' already exists",
        )

class ValidationFailedError(HTTPException):
    def __init__(self, errors: list):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=errors,
        )

class UnauthorizedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

class ForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden",
        )

class InternalServerError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal Server Error",
        )
