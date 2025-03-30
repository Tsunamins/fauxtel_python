from sqlalchemy.orm import Session
from app.schemas import schemas
from app.models import User
from app.security import get_password_hash, verify_password

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        phone_number=user.phone_number,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if user and verify_password(password, user.hashed_password):
        return user
    return None

def update_user(db: Session, user_id: str, user: schemas.UserCreate):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.email = user.email
        db_user.first_name = user.first_name
        db_user.last_name = user.last_name
        db_user.address = user.address
        db_user.phone_number = user.phone_number

        if user.password:
            db_user.hashed_password = get_password_hash(user.password)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def delete_user(db: Session, user_id: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None