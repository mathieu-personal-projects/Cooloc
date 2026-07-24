from fastapi import APIRouter, Depends
from typing import Dict
from src.models.api.ApiResponse import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_connection import get_db


router = APIRouter()

@router.get("/", response_model=ApiResponse[dict])
async def get_hello(db: AsyncSession = Depends(get_db)) -> ApiResponse[dict]:
    return ApiResponse(
        statusCode=200,
        message="successfully called the Hello World endpoint",
        data={
            "Hello": "World!",
            "dbStatus": "OK"
        }
    )