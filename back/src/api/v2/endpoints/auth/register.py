from fastapi import APIRouter, Depends
from typing import Dict
from src.models.api.ApiResponse import ApiResponse
from src.models.api.ApiRequest import ApiRequest
from src.models.payloads.user import UserRegisterPayload
from src.services.auth import register_user
from src.core.db_connection import get_db
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

@router.post("/register", response_model=ApiResponse[dict])
async def register(request: ApiRequest[UserRegisterPayload], db: AsyncSession = Depends(get_db)) -> ApiResponse[dict]:
    if not request.data:
        return ApiResponse(
            statusCode=400,
            message="Bad request",
            data={
                "errorMessage": "No data sent"
            }
        )

    try:
        result = await register_user(db=db, payload=request.data)

        return ApiResponse(
                statusCode=200,
                message="Successfully registered user",
                data={
                    "id": result["id"],
                    "first_name": result["first_name"],
                    "last_name": result["last_name"],
                    "role": result["role"],
                    "jwtToken": result["jwtToken"]
                }
            )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to register user",
            data={
                "errorMessage": str(e)
            }
        )