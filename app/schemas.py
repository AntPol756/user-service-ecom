from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(..., ge=0, le=130)
    address: str = Field(..., min_length=1, max_length=255)
    # the date the user joined the company as a customer (defaults to now)
    joining_date: Optional[datetime] = None


class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    age: Optional[int] = Field(None, ge=0, le=130)
    address: Optional[str] = Field(None, min_length=1, max_length=255)
    joining_date: Optional[datetime] = None


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    address: str
    joining_date: datetime
    is_registered: bool

    model_config = ConfigDict(from_attributes=True)