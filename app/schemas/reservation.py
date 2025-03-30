from pydantic import BaseModel
from datetime import datetime
from typing import List, Tuple, Optional

class ReservationBase(BaseModel):
    reservation_code: str
    room_id: str
    location_id: str
    date_ranges: List[Tuple[datetime, datetime]]

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True


class ReservationUpdate(BaseModel):
    room_id: Optional[str] = None
    location_id: Optional[str] = None
    date_ranges: Optional[List] = None

    class Config:
        from_attributes = True

