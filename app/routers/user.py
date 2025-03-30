from app.auth.auth import create_access_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserResponse, UserCreate, UserUpdateResponse
from app import services
from app.database import SessionLocal
from datetime import timedelta
from app.auth import get_password_hash


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register/", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = services.user_service.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return services.user_service.create_user(db, user)

@router.post("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = services.user_service.authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.email}, timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}

@router.put("/user/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user_update: UserUpdateResponse, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.email:
        db_user.email = user_update.email
    if user_update.first_name:
        db_user.first_name = user_update.first_name
    if user_update.last_name:
        db_user.last_name = user_update.last_name
    if user_update.address:
        db_user.address = user_update.address
    if user_update.phone_number:
        db_user.phone_number = user_update.phone_number
    
    # If password is provided, hash it before updating
    if user_update.password:
        db_user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/delete/{user_id}", response_model=UserResponse)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = services.user_service.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
