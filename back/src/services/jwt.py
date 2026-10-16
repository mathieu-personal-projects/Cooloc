import jwt
from datetime import datetime, timedelta, timezone
from src.config import JWT_ALGO, settings

ACCESS_TOKEN_EXPIRE_MINUTES = 60


def create_token(user_id: str, email: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    claims = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(claims, settings.JWT_SIGNATURE, algorithm=JWT_ALGO)


def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.JWT_SIGNATURE, algorithms=[JWT_ALGO])