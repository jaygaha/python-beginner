from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enums.user_enum import UserStatus

"""
This class represents a user model.
"""
class UserBase(BaseModel):
    username: str = Field(..., title="Username", description="The username of the user", min_length=3, max_length=100)
    email: str = Field(..., title="Email", description="The email address of the user", pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    full_name: Optional[str] = None
    age: int = Field(..., title="Age", description="The age of the user", ge=0, le=120)
    status: UserStatus = UserStatus.ACTIVE

class UserCreate(UserBase):
    password: str = Field(..., title="Password", description="The password of the user", min_length=8, max_length=100)

class UserResponse(UserBase):
    id: int
    is_active: bool = True
    created_at: datetime

    class ConfigDict:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[str] = Field(None, pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    full_name: Optional[str] = None

class UsersListResponse(BaseModel):
    users: List[UserResponse]
    total: int
    skip: int
    limit: int
