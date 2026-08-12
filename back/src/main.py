from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from src.config import settings
from src.api.v2.router import api_router
from src.models.api.ApiResponse import ApiResponse
from typing import Dict


app = FastAPI(title=settings.APP_NAME, description="Api to handle Cooloc's backend", docs_url=f"{settings.API_PREFIX}/docs")
app.include_router(api_router, prefix=settings.API_PREFIX)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, e: Exception) -> JSONResponse:
    detail = str(e) if settings.DEBUG else "Internal error occurred."
    
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"statusCode": 500, "errorMessage": f"{e.__class__.__name__}", "data": detail})

@app.get(settings.API_PREFIX, response_model=ApiResponse[dict])
def read_root() -> ApiResponse[dict]:
    return ApiResponse(
        statusCode=200,
        message="successfully called the api root",
        data={
            "app": settings.APP_NAME,
            "version": settings.VERSION
        }
    )