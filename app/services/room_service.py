from sqlalchemy.orm import Session
from app.schemas import RoomCreate
from app.models import Room

def get_room(db: Session, room_id: str):
    return db.query(Room).filter(Room.id == room_id).first()

def get_rooms(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Room).offset(skip).limit(limit).all()

def create_room(db: Session, room: RoomCreate):
    db_room = Room(**room.model_dump())
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

def update_room(db: Session, room_id: str, room: RoomCreate):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if db_room:
        for key, value in room.model_dump().items():
            setattr(db_room, key, value)
        db.commit()
        db.refresh(db_room)
    return db_room

def delete_room(db: Session, room_id: str):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if db_room:
        db.delete(db_room)
        db.commit()
    return db_room