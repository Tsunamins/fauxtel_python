from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    address: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    reservations: List[int] = []  # Will store reservation IDs

    class Config:
        from_attributes = True


class UserUpdateResponse(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True