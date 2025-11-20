"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

# Cafe Website Schemas

class Reservation(BaseModel):
    """
    Reservations collection schema
    Collection name: "reservation"
    """
    name: str = Field(..., description="Guest full name", min_length=2)
    email: EmailStr = Field(..., description="Contact email")
    phone: str = Field(..., description="Phone number")
    date: str = Field(..., description="Reservation date (YYYY-MM-DD)")
    time: str = Field(..., description="Reservation time (HH:MM)")
    party_size: int = Field(..., ge=1, le=20, description="Number of guests")
    notes: Optional[str] = Field(None, description="Additional notes or requests")

class Message(BaseModel):
    """
    Contact messages collection schema
    Collection name: "message"
    """
    name: str = Field(..., description="Sender name", min_length=2)
    email: EmailStr = Field(..., description="Sender email")
    message: str = Field(..., min_length=5, description="Message content")

# Example schemas (kept for reference if needed in future)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
