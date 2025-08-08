from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.database.crud import get_user_by_id, update_user
from src.schemas.user import UserUpdate, User
from src.models.user import User as UserModel
from typing import Optional

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_current_user(self, user_id: int) -> User:
        """Get current user by ID"""
        user = get_user_by_id(self.db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return User.from_orm(user)

    def update_current_user(self, user_id: int, user_update: UserUpdate) -> User:
        """Update current user"""
        updated_user = update_user(self.db, user_id, user_update)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return User.from_orm(updated_user)
