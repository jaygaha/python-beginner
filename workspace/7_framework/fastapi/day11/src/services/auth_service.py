from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from src.database.crud import get_user_by_username, create_user
from src.schemas.user import UserCreate
from src.schemas.token import Token
from src.core.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from typing import Optional

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, username: str, password: str) -> Optional[dict]:
        """Authenticate user with username and password"""
        user = get_user_by_username(self.db, username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Inactive user"
            )
        return {"user_id": user.id, "username": user.username}

    def register_user(self, user_data: UserCreate) -> Token:
        """Register new user"""
        # Check if user already exists
        if get_user_by_username(self.db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )

        # Create user
        db_user = create_user(self.db, user_data)

        # Generate tokens
        access_token = create_access_token(subject=db_user.id)
        refresh_token = create_refresh_token(subject=db_user.id)

        return Token(access_token=access_token, refresh_token=refresh_token)

    def login_user(self, username: str, password: str) -> Token:
        """Login user and return tokens"""
        user_data = self.authenticate_user(username, password)
        if not user_data:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(subject=user_data["user_id"])
        refresh_token = create_refresh_token(subject=user_data["user_id"])

        return Token(access_token=access_token, refresh_token=refresh_token)

    def refresh_token(self, refresh_token: str) -> Token:
        """Refresh access token"""
        user_id = verify_token(refresh_token, token_type="refresh")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token = create_access_token(subject=user_id)
        new_refresh_token = create_refresh_token(subject=user_id)

        return Token(access_token=access_token, refresh_token=new_refresh_token)
