from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.services import reservation_service
from app.database import SessionLocal, engine
from app.models import Base

# Create the tables in the database
Base.metadata.create_all(bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reservations/", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    return reservation_service.create_reservation(db=db, reservation=reservation)

@router.get("/reservations/", response_model=List[schemas.Reservation])
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = reservation_service.get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.get("/reservations/{reservation_id}", response_model=schemas.Reservation)
def read_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = reservation_service.get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.put("/reservations/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: str, reservation: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = reservation_service.update_reservation(db, reservation_id, reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.delete("/reservations/{reservation_id}", response_model=schemas.Reservation)
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = reservation_service.delete_reservation(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation