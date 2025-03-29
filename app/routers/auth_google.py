from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.orm import Session
import requests
from app import models, schemas, services
from app.database import get_db

GOOGLE_CLIENT_ID = "your_google_client_id"
GOOGLE_CLIENT_SECRET = "your_google_client_secret"
GOOGLE_REDIRECT_URI = "your_redirect_uri"

router = APIRouter()

@router.get("/google-login/")
def google_login():
    return {
        "auth_url": f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=email profile"
    }

@router.get("/google-callback/")
def google_callback(code: str, db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    
    token_response = requests.post(token_url, data=token_data).json()
    access_token = token_response.get("access_token")
    
    user_info = requests.get(
        "https://www.googleapis.com/oauth2/v2/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    ).json()
    
    if not user_info.get("email"):
        raise HTTPException(status_code=400, detail="Google authentication failed")
    
    db_user = services.user_service.get_user_by_email(db, user_info["email"])
    if not db_user:
        db_user = services.user_service.create_user(
            db,
            schemas.UserCreate(
                email=user_info["email"],
                password="google_oauth",  # No password needed for OAuth users
                first_name=user_info.get("given_name", ""),
                last_name=user_info.get("family_name", ""),
                address="",
                phone_number="",
            ),
        )

    access_token = create_access_token({"sub": db_user.email}, timedelta(minutes=60))
    return {"access_token": access_token, "token_type": "bearer"}
