from sqlalchemy import Column, Integer, String, Boolean, DateTime
from database.database import Base
from datetime import datetime

class NewsletterSubscription(Base):
    __tablename__ = "newsletter_subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255) , unique=True , nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
