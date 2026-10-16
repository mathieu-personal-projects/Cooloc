from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.models.payloads.user import UserRegisterPayload, UserLoginPayload
from src.models.User import User
from src.models.api.ApiResponse import ApiResponse
from src.services.jwt import create_token
import bcrypt


def hash_password(passwd: str) -> str:
    passwd_bytes = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt(12))
    return passwd_bytes.decode('utf-8')

async def register_user(db: AsyncSession, payload: UserRegisterPayload) -> Dict[any]:
    if not payload.csrfToken:
        hasCsrfToken = True if payload.csrfToken else False
        return ApiResponse(
            statusCode=401,
            message="Unauthorized",
            data={
                "errorMessage": "missing or no csrfToken provided",
                "hasCsrf": hasCsrfToken            
            }
        )

    existing_mail_query = await db.execute(text("SELECT email FROM users WHERE email = :email"), params={"email": payload.email}) 
    exist_mail_row = existing_mail_query.first()
    if exist_mail_row:
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

    jwtToken = create_token(payload=payload)

    user = User(
        email=payload.email,
        password_hash=hash_password(payload.password),
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone_number=payload.phone_number,
        global_role=payload.global_role,
    )

    register_user_query = await db.execute(
        text("INSERT INTO users (email, password_hash, first_name, last_name, phone_number, global_role) VALUES(:email, :password_hash, :first_name, :last_name, :phone_number, :global_role)"), 
        params={
            "email": user.email,
            "password_hash": user.password_hash,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "phone_number": user.phone_number,
            "global_role": user.global_role.value
        }
    )
    await db.commit()

    # TODO: implement automatical login ? 
    id_query = await db.execute(text("SELECT id FROM users WHERE email = :email"), params={"email": user.email}) 
    id_user_row = id_query.first()
    id_user = id_user_row[0] if id_user_row else None

    result = {
        "id": id_user,
        "email": user.email,
        "password_hash": user.password_hash,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "global_role": user.global_role.value
    }

    return ApiResponse(
        statusCode=200,
        message="OK",
        data={
            "jwtToken": jwtToken,
            "data": result            
        }
    )

async def login_user(db: AsyncSession, payload: UserLoginPayload) -> ApiResponse:
    if not payload.csrfToken:
        return ApiResponse(
            statusCode=401,
            message="Unauthorized",
            data={"errorMessage": "missing or no csrfToken provided", "hasCsrf": False},
        )

    query = await db.execute(
        text(
            "SELECT id, email, password_hash, first_name, last_name, global_role, phone_number "
            "FROM users WHERE email = :email LIMIT 1"
        ),
        params={"email": payload.email},
    )
    user = query.first()

    if not user or not bcrypt.checkpw(
        payload.password.encode("utf-8"),
        user.password_hash.encode("utf-8"),
    ):
        return ApiResponse(
            statusCode=401,
            message="Unable to login",
            data={"errorMessage": "invalid email or password"},
        )

    role = getattr(user.global_role, "value", user.global_role)
    jwtToken = create_token(user_id=str(user.id), email=user.email, role=role)

    return ApiResponse(
        statusCode=200,
        message="OK",
        data={
            "jwtToken": jwtToken,
            "data": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "global_role": role,
                "phone_number": user.phone_number,
            },
        },
    )