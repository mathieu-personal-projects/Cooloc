# this is a sort of router 
from fastapi import APIRouter
from src.api.v2.endpoints import hello 

api_router = APIRouter()

api_router.include_router(hello.router, prefix="/hello", tags=["hello"])

