from fastapi import APIRouter
from typing import Dict
from src.models.ApiResponse import ApiResponse


router = APIRouter()

@router.get("/", response_model=ApiResponse[dict])
def get_hello() -> ApiResponse[dict]:
    return ApiResponse(
        statusCode=200,
        message="successfully called the Hello World endpoint",
        data={
            "Hello": "World!"
        }
    )