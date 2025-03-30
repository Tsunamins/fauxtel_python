from sqlalchemy.orm import Session
from app.schemas import ReservationCreate
from app.models import Reservation

def get_reservation(db: Session, reservation_id: str):
    return db.query(Reservation).filter(Reservation.id == reservation_id).first()

def get_reservations(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Reservation).offset(skip).limit(limit).all()

def create_reservation(db: Session, reservation: ReservationCreate):
    db_reservation = Reservation(**reservation.model_dump())
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

def update_reservation(db: Session, reservation_id: str, reservation: ReservationCreate):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation:
        for key, value in reservation.model_dump().items():
            setattr(db_reservation, key, value)
        db.commit()
        db.refresh(db_reservation)
    return db_reservation

def delete_reservation(db: Session, reservation_id: str):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation:
        db.delete(db_reservation)
        db.commit()
    return db_reservation