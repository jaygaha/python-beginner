from enum import Enum

class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class SortOrder(str, Enum):
    ASC = "asc"
    DESC = "desc"
