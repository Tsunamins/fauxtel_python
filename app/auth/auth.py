import bcrypt
from datetime import datetime, timedelta
from authlib.jose import jwt

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')  # Decode to return a string

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc)+ expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode({"alg": ALGORITHM}, SECRET_KEY, to_encode)
    return encoded_jwt
