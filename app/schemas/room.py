from pydantic import BaseModel
from typing import Optional

class RoomBase(BaseModel):
    room_number: int
    room_type: str
    room_description: str

class RoomCreate(RoomBase):
    location_id: str

class Room(RoomBase):
    id: str
    location_id: str

    class Config:
        from_attributes = True


class RoomUpdateResponse(BaseModel):
    room_number: Optional[int] = None
    room_type: Optional[str] = None
    room_description: Optional[str] = None

    class Config:
        from_attributes = True