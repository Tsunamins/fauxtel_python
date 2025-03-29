from pydantic import BaseModel
from datetime import datetime

class LocationBase(BaseModel):
    name: str
    description: str
    city: str
    state: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class RoomBase(BaseModel):
    room_number: int
    room_type: str
    room_description: str

class RoomCreate(RoomBase):
    pass

class Room(RoomBase):
    id: int
    location_id: int

    class Config:
        orm_mode = True


from pydantic import BaseModel
from datetime import datetime
from typing import List, Tuple

class ReservationBase(BaseModel):
    reservation_code: str
    room_id: int
    location_id: int
    date_ranges: List[Tuple[datetime, datetime]]

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


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