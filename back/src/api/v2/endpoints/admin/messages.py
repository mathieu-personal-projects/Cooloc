from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_connection import get_db
from src.models.api.ApiResponse import ApiResponse
from src.models.api.ApiRequest import ApiRequest
from src.models.payloads.message import MessageGetPayload
from src.core.auth import require_admin

router = APIRouter()


@router.get("/messages", response_model=ApiResponse[dict])
async def get_messages(db: AsyncSession = Depends(get_db), _admin: dict = Depends(require_admin)) -> ApiResponse[dict]:
    try:
        result = await db.execute(
            text(
                "SELECT * "
                "FROM messages ORDER BY id;"
            )
        )
        messages = [dict(row) for row in result.mappings().all()]

        return ApiResponse(
            statusCode=200,
            message="Successfully retrieved messages",
            data={"messages": messages},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to retrieve messages",
            data={"errorMessage": str(e)},
        )

@router.post("/message", response_model=ApiResponse[dict])
async def get_message(request: ApiRequest[MessageGetPayload], db: AsyncSession = Depends(get_db), _admin: dict = Depends(require_admin)) -> ApiResponse[dict]:
    if not request.data:
        return ApiResponse(
            statusCode=400,
            message="Bad request",
            data={"errorMessage": "No data sent"},
        )

    try:
        result = await db.execute(
            text(
                "SELECT * "
                "FROM message WHERE id = :id LIMIT 1;"
            ),
            params={"id": request.data.id},
        )
        message = result.mappings().first()

        if not message:
            return ApiResponse(
                statusCode=404,
                message="message not found",
                data={"errorMessage": "no message with this id"},
            )

        return ApiResponse(
            statusCode=200,
            message="Successfully retrieved message",
            data={"message": dict(message)},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to retrieve message",
            data={"errorMessage": str(e)},
        )