from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app import models, database, utils

# ---------------- JWT SETTINGS ----------------
SECRET_KEY = "your_super_secret_key_here"  # ⚠️ Change this before deployment!
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------- OAUTH2 ----------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

# ---------------- JWT TOKEN CREATION ----------------
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Create JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------------- VERIFY USER FROM TOKEN ----------------
def get_current_user(db: Session = Depends(database.get_db), token: str = Depends(oauth2_scheme)):
    """Extract current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user

# ---------------- PASSWORD HELPERS (from utils) ----------------
def hash_password(password: str):
    """Wrapper for utils.hash_password"""
    return utils.hash_password(password)

def verify_password(plain_password: str, hashed_password: str):
    """Wrapper for utils.verify_password"""
    return utils.verify_password(plain_password, hashed_password)
