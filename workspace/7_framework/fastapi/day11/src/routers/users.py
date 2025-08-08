from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.database.connection import get_db
from src.schemas.user import User, UserUpdate
from src.services.user_service import UserService
from src.routers.dependencies import get_current_user, get_current_superuser
from src.models.user import User as UserModel

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=User)
async def read_current_user(
    current_user: UserModel = Depends(get_current_user)
):
    """Get current user profile"""
    return User.from_orm(current_user)

@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    user_service = UserService(db)
    return user_service.update_current_user(current_user.id, user_update)

@router.get("/admin-only")
async def admin_only_endpoint(
    current_superuser: UserModel = Depends(get_current_superuser)
):
    """Example admin-only endpoint"""
    return {"message": "Hello, admin!", "user": current_superuser.username}
