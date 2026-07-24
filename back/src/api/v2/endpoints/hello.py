from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from src.models.api.ApiResponse import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.core.db_connection import get_db


router = APIRouter()

@router.get("/", response_model=ApiResponse[dict])
async def get_hello(db: AsyncSession = Depends(get_db)) -> ApiResponse[dict]:
    try: 
        await db.execute(text("SELECT 1"))
        
        return ApiResponse(
                statusCode=200,
                message="successfully called the Hello World endpoint",
                data={
                    "Hello": "World!",
                    "dbStatus": "OK"
                }
            )

    except Exception as e:
        return ApiResponse(
                statusCode=500,
                message="Unable to call Hello World and the db",
                data={
                    "errorMessage": str(e)
                }
            )