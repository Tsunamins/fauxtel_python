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