from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.database import get_db
from app.security import create_access_token
from datetime import timedelta

router = APIRouter()

@router.post("/register/", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
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
