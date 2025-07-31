from src.enums.user_enum import UserStatus, SortOrder


def test_user_status_enum_values():
    assert UserStatus.ACTIVE == "active"
    assert UserStatus.INACTIVE == "inactive"
    assert UserStatus.SUSPENDED == "suspended"

def test_user_status_enum_string_representation():
    assert UserStatus.ACTIVE == "active"
    assert UserStatus.INACTIVE == "inactive"
    assert UserStatus.SUSPENDED == "suspended"

def test_user_status_enum_membership():
    assert "active" in UserStatus
    assert "inactive" in UserStatus
    assert "suspended" in UserStatus
    assert "invalid" not in UserStatus

def test_user_status_enum_type():
    assert isinstance(UserStatus.ACTIVE, UserStatus)
    assert isinstance(UserStatus.ACTIVE, str)

def test_sort_order_enum_values():
    assert SortOrder.ASC == "asc"
    assert SortOrder.DESC == "desc"

def test_sort_order_enum_string_representation():
    assert SortOrder.ASC.value == "asc"
    assert SortOrder.DESC.value == "desc"

def test_sort_order_enum_membership():
    assert "asc" in SortOrder
    assert "desc" in SortOrder
    assert "invalid" not in SortOrder

def test_sort_order_enum_type():
    assert isinstance(SortOrder.ASC, SortOrder)
    assert isinstance(SortOrder.ASC, str)
