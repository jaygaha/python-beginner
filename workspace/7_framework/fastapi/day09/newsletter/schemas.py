from pydantic import BaseModel, EmailStr
from datetime import datetime

class NewsletterSubscriptionBase(BaseModel):
    email: EmailStr # A built-in type from Pydantic that validates email formats.

class NewsletterSubscriptionCreate(NewsletterSubscriptionBase):
    # Simulate subscription creation
    pass

class NewsletterSubscriptionResponse(NewsletterSubscriptionBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
