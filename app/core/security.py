# security.py
from pwdlib import PasswordHash
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError

from app.core.constants import (
    SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES
)

# Initialize PasswordHash with modern, secure default settings
password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    """Generates a secure hash from a plain-text password."""
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies if the provided plain password matches the stored hash."""
    return password_hash.verify(plain_password, hashed_password)


# JWT token
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({
        "exp": expire
    })

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return {}
    

    