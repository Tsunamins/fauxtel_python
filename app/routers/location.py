from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import Location, LocationCreate, LocationUpdate
from app.services import location_service
from app.database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/locations/", response_model=Location)
def create_location(location: LocationCreate, db: Session = Depends(get_db)):
    return location_service.create_location(db=db, location=location)

@router.get("/locations/", response_model=List[Location])
def read_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    locations = location_service.get_locations(db, skip=skip, limit=limit)
    return locations

@router.get("/locations/{location_id}", response_model=Location)
def read_location(location_id: str, db: Session = Depends(get_db)):
    db_location = location_service.get_location(db, location_id=location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location


@router.put("/location/{location_id}", response_model=Location)
def update_location(location_id: str, location_update: LocationUpdate, db: Session = Depends(get_db)):
    db_location = db.query(Location).filter(Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="Location not found")
    
    if location_update.name:
        db_location.name = location_update.name
    if location_update.description:
        db_location.description = location_update.description
    if location_update.city:
        db_location.city = location_update.city
    if location_update.state:
        db_location.state = location_update.state

    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/locations/{location_id}", response_model=Location)
def delete_location(location_id: str, db: Session = Depends(get_db)):
    db_location = location_service.delete_location(db, location_id)
    if db_location is None:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_location