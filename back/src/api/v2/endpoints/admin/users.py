from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_connection import get_db
from src.models.api.ApiResponse import ApiResponse
from src.models.api.ApiRequest import ApiRequest
from src.models.payloads.user import UserGetPayload
from src.core.auth import require_admin

router = APIRouter()


@router.get("/users", response_model=ApiResponse[dict])
async def get_users(db: AsyncSession = Depends(get_db), _admin: dict = Depends(require_admin)) -> ApiResponse[dict]:
    try:
        result = await db.execute(
            text(
                "SELECT id, email, first_name, last_name, phone_number, global_role "
                "FROM users ORDER BY id;"
            )
        )
        users = [dict(row) for row in result.mappings().all()]

        return ApiResponse(
            statusCode=200,
            message="Successfully retrieved users",
            data={"users": users},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to retrieve users",
            data={"errorMessage": str(e)},
        )

@router.post("/user", response_model=ApiResponse[dict])
async def get_user(request: ApiRequest[UserGetPayload], db: AsyncSession = Depends(get_db), _admin: dict = Depends(require_admin)) -> ApiResponse[dict]:
    if not request.data:
        return ApiResponse(
            statusCode=400,
            message="Bad request",
            data={"errorMessage": "No data sent"},
        )

    try:
        result = await db.execute(
            text(
                "SELECT id, email, first_name, last_name, phone_number, global_role "
                "FROM users WHERE id = :id LIMIT 1;"
            ),
            params={"id": request.data.id},
        )
        user = result.mappings().first()

        if not user:
            return ApiResponse(
                statusCode=404,
                message="User not found",
                data={"errorMessage": "no user with this id"},
            )

        return ApiResponse(
            statusCode=200,
            message="Successfully retrieved user",
            data={"user": dict(user)},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to retrieve user",
            data={"errorMessage": str(e)},
        )