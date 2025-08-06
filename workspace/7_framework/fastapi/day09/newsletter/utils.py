from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException, status

def create_subscription(db: Session, subscription: schemas.NewsletterSubscriptionCreate):
    db_subscription = models.NewsletterSubscription(
        email=subscription.email
    )
    try:
        db.add(db_subscription)
        db.commit()
        db.refresh(db_subscription)
        return db_subscription
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already subscribed"
        )

def get_subscription(db: Session, email: str):
    return db.query(models.NewsletterSubscription).filter(
        models.NewsletterSubscription.email == email
    ).first()

def get_all_subscriptions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.NewsletterSubscription).offset(skip).limit(limit).all()

def delete_subscription(db: Session, email: str):
    subscription = get_subscription(db, email)
    if subscription:
        db.delete(subscription)
        db.commit()
        return True
    return False
