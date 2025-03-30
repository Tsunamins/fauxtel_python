from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LocationBase(BaseModel):
    name: str
    description: str
    city: str
    state: str

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class LocationUpdate(BaseModel):
    name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    description: Optional[str] = None

    class Config:
        from_attributes = True
