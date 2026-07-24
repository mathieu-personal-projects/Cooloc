from fastapi import APIRouter
from src.api.v2.endpoints import hello 
from src.api.v2.endpoints.auth import register


api_router = APIRouter()

api_router.include_router(hello.router, prefix="/hello", tags=["hello"])

api_router.include_router(register.router, prefix="/auth", tags=["auth"])