import pytest
from fastapi import HTTPException, status
from src.exceptions import (
    ItemNotFoundError,
    InsufficientStockError,
    DuplicateItemError,
    ValidationFailedError,
    UnauthorizedError,
    ForbiddenError,
    InternalServerError,
)

def test_item_not_found_error():
    item_id = 123
    with pytest.raises(ItemNotFoundError) as exc_info:
        raise ItemNotFoundError(item_id=item_id)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert exc_info.value.detail == f"Item with ID {item_id} not found"
    assert isinstance(exc_info.value, HTTPException)

def test_insufficient_stock_error():
    item_id, requested, available = 123, 10, 5
    with pytest.raises(InsufficientStockError) as exc_info:
        raise InsufficientStockError(item_id=item_id, requested=requested, available=available)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert exc_info.value.detail == f"Insufficient stock for item {item_id}. Requested: {requested}, Available: {available}"
    assert isinstance(exc_info.value, HTTPException)

def test_duplicate_item_error():
    field, value = "name", "test_item"
    with pytest.raises(DuplicateItemError) as exc_info:
        raise DuplicateItemError(field=field, value=value)
    assert exc_info.value.status_code == status.HTTP_409_CONFLICT
    assert exc_info.value.detail == f"Item with ID {field} '{value}' already exists"
    assert isinstance(exc_info.value, HTTPException)

def test_validation_failed_error():
    errors = [{"loc": ["body", "name"], "msg": "field required"}]
    with pytest.raises(ValidationFailedError) as exc_info:
        raise ValidationFailedError(errors=errors)
    assert exc_info.value.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert exc_info.value.detail == errors
    assert isinstance(exc_info.value, HTTPException)

def test_unauthorized_error():
    with pytest.raises(UnauthorizedError) as exc_info:
        raise UnauthorizedError()
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Unauthorized"
    assert isinstance(exc_info.value, HTTPException)

def test_forbidden_error():
    with pytest.raises(ForbiddenError) as exc_info:
        raise ForbiddenError()
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    assert exc_info.value.detail == "Forbidden"
    assert isinstance(exc_info.value, HTTPException)

def test_internal_server_error():
    with pytest.raises(InternalServerError) as exc_info:
        raise InternalServerError()
    assert exc_info.value.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert exc_info.value.detail == "Internal Server Error"
    assert isinstance(exc_info.value, HTTPException)
