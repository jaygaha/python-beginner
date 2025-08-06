from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.database import get_db
from .schemas import NewsletterSubscriptionBase , NewsletterSubscriptionCreate , NewsletterSubscriptionResponse
from .utils import create_subscription , get_all_subscriptions , delete_subscription
router = APIRouter(prefix="/newsletter", tags=["newsletter"])

@router.post("/subscribe", response_model=NewsletterSubscriptionResponse)
def subscribe(
    subscription: NewsletterSubscriptionCreate,
    db: Session = Depends(get_db)
):

    return create_subscription(db, subscription)

@router.get("/subscriptions", response_model=list[NewsletterSubscriptionResponse])
def get_subscriptions(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return get_all_subscriptions(db, skip, limit)

@router.delete("/unsubscribe/{email}")
def unsubscribe(email: str, db: Session = Depends(get_db)):
    if delete_subscription(db, email):
        return {"message": "Successfully unsubscribed"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Subscription not found"
    )
