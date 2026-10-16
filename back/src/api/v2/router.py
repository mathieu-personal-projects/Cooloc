from fastapi import APIRouter
from src.api.v2.endpoints import hello 
from src.api.v2.endpoints.auth import register, login
from src.api.v2.endpoints.admin import users, tasks, messages, colocations, correlated


api_router = APIRouter()

api_router.include_router(hello.router, prefix="/hello", tags=["hello"])

api_router.include_router(register.router, prefix="/auth", tags=["auth"])
api_router.include_router(login.router, prefix="/auth", tags=["auth"])

api_router.include_router(users.router, prefix="/admin", tags=["admin"])
api_router.include_router(tasks.router, prefix="/admin", tags=["admin"])
api_router.include_router(messages.router, prefix="/admin", tags=["admin"])
api_router.include_router(colocations.router, prefix="/admin", tags=["admin"])
api_router.include_router(correlated.router, prefix="/admin", tags=["admin"])