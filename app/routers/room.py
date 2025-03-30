from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import Room, RoomCreate, RoomUpdateResponse
from app.services import room_service
from app.database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/rooms/", response_model=Room)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    return room_service.create_room(db=db, room=room)

@router.get("/rooms/", response_model=List[Room])
def read_rooms(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = room_service.get_rooms(db, skip=skip, limit=limit)
    return locations

@router.get("/rooms/{room_id}", response_model=Room)
def read_room(room_id: str, db: Session = Depends(get_db)):
    db_room = room_service.get_room(db, room_id=room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room

@router.put("/rooms/{room_id}", response_model=Room)
def update_room(room_id: str, room_update: RoomUpdateResponse, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if not db_room:
        raise HTTPException(status_code=404, detail="Location not found")
    
    if db_room.room_number:
        db_room.room_number = db_room.room_number
    if db_room.room_type:
        db_room.room_type = db_room.room_type
    if db_room.room_description:
        db_room.room_description = db_room.room_description

    db.commit()
    db.refresh(db_room)
    return db_room

@router.delete("/rooms/{room_id}", response_model=Room)
def delete_room(room_id: str, db: Session = Depends(get_db)):
    db_room = room_service.delete_room(db, room_id)
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return db_room