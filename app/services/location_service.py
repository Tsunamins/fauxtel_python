from sqlalchemy.orm import Session
from app.schemas import LocationCreate
from app.models import Location

def get_location(db: Session, location_id: str):
    return db.query(Location).filter(Location.id == location_id).first()

def get_locations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Location).offset(skip).limit(limit).all()

def create_location(db: Session, location: LocationCreate):
    db_location = Location(**location.model_dump())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

def update_location(db: Session, location_id: str, location: LocationCreate):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location:
        for key, value in location.model_dump().items():
            setattr(db_location, key, value)
        db.commit()
        db.refresh(db_location)
    return db_location

def delete_location(db: Session, location_id: str):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if db_location:
        db.delete(db_location)
        db.commit()
    return db_location