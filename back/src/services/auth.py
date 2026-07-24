from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.models.payloads.user import UserRegisterPayload
from src.models.User import User
from src.models.api.ApiResponse import ApiResponse
import bcrypt


def hash_password(passwd: str) -> str:
    passwd = bcrypt.hashpw(passwd, bcrypt.gensalt(12))
    return passwd

async def register_user(db: AsyncSession, payload: UserRegisterPayload) -> Dict[any]:
    # check csrf

    existing_mail = await db.execute(text("SELECT mail FROM users WHERE mail = %s"), params=payload.email) 
    if existing_mail:
        return ApiResponse(
            statusCode=400,
            message="Unable to create account",
            data={
                "errorMessage": "email already exists"
            }
        )
    
    if len(payload.password) < 14:
        return ApiResponse(
            statusCode=400,
            message="Unable to create account",
            data={
                "errorMessage": "password is too short (< 14 char)"
            }
        )

    # create jwtToken
    jwtToken = "caca"

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone_number=payload.phone_number,
        global_role=payload.global_role,
    )

    result = {
        "jwtToken": jwtToken,
        "data": user
    }

    return result