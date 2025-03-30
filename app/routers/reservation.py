from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import ReservationCreate, ReservationUpdate, Reservation
from app.services import reservation_service
from app.database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reservations/", response_model=Reservation)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    return reservation_service.create_reservation(db=db, reservation=reservation)

@router.get("/reservations/", response_model=List[Reservation])
def read_reservations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    reservations = reservation_service.get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.get("/reservations/{reservation_id}", response_model=Reservation)
def read_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = reservation_service.get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.put("/reservations/{reservation_id}", response_model=Reservation)
def update_room(reservation_id: str, room_update: ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not db_reservation:
        raise HTTPException(status_code=404, detail="Location not found")
    
    if db_reservation.room_id:
        db_reservation.room_id = db_reservation.room_id
    if db_reservation.location_id:
        db_reservation.location_id = db_reservation.location_id
    if db_reservation.date_ranges:
        db_reservation.date_ranges = db_reservation.date_ranges

    db.commit()
    db.refresh(db_reservation)
    return db_reservation


@router.put("/reservations/{reservation_id}", response_model=Reservation)
def update_reservation(reservation_id: str, reservation: ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = reservation_service.update_reservation(db, reservation_id, reservation)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation

@router.delete("/reservations/{reservation_id}", response_model=Reservation)
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = reservation_service.delete_reservation(db, reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return db_reservation