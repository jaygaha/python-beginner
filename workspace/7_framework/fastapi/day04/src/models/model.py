from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., gt=0)
    category: str
    tags: List[str] = []

class ProductCreate(ProductBase):
    pass # simulate creation

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

class UserProfile(BaseModel):
    bio: Optional[str] = None
    website: Optional[str] = None
    location: Optional[str] = None
    birth_date: Optional[datetime] = None

class ContactForm(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: str = Field(..., pattern=r'^[\w\.-]+@[\w\.-]+\.\w+$')
    subject: str = Field(..., min_length=5, max_length=100)
    message: str = Field(..., min_length=10, max_length=1000)
    urgent: bool = False
