import urllib.parse
import urllib.request
import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, services
from app.database import SessionLocal

GOOGLE_CLIENT_ID = "your_google_client_id"
GOOGLE_CLIENT_SECRET = "your_google_client_secret"
GOOGLE_REDIRECT_URI = "your_redirect_uri"

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/google-login/")
def google_login():
    auth_url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&scope=email profile"
    return {"auth_url": auth_url}

@router.get("/google-callback/")
def google_callback(code: str, db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    
    token_data = {
        "code": code,
        "client_id": GOOGLE_CLIENT_ID,
        "client_secret": GOOGLE_CLIENT_SECRET,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code"
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    token_data_encoded = urllib.parse.urlencode(token_data).encode()

    request = urllib.request.Request(token_url, data=token_data_encoded, headers=headers)
    
    try:
        with urllib.request.urlopen(request) as response:
            token_response = json.load(response)
    except urllib.error.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to get token: {e.reason}")

    access_token = token_response.get("access_token")
    
    if not access_token:
        raise HTTPException(status_code=400, detail="Google authentication failed")

    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    request = urllib.request.Request(
        user_info_url,
        headers={"Authorization": f"Bearer {access_token}"}
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            user_info = json.load(response)
    except urllib.error.HTTPError as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch user info: {e.reason}")

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
