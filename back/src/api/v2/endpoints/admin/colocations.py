from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_connection import get_db
from src.models.api.ApiResponse import ApiResponse
from src.models.api.ApiRequest import ApiRequest
from src.models.payloads.colocation import ColocationGetPayload
from src.core.auth import require_admin

router = APIRouter()


@router.get("/colocations", response_model=ApiResponse[dict])
async def get_colocations(db: AsyncSession = Depends(get_db), _admin: dict = Depends(require_admin)) -> ApiResponse[dict]:
    try:
        result = await db.execute(
            text(
                "SELECT * "
                "FROM colocations ORDER BY id;"
            )
        )
        colocations = [dict(row) for row in result.mappings().all()]

        return ApiResponse(
            statusCode=200,
            colocation="Successfully retrieved colocations",
            data={"colocations": colocations},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            colocation="Unable to retrieve colocations",
            data={"errorcolocation": str(e)},
        )

@router.post("/colocation", response_model=ApiResponse[dict])
async def get_colocation(request: ApiRequest[ColocationGetPayload], db: AsyncSession = Depends(get_db), _admin: dict = Depends(require_admin)) -> ApiResponse[dict]:
    if not request.data:
        return ApiResponse(
            statusCode=400,
            colocation="Bad request",
            data={"errorcolocation": "No data sent"},
        )

    try:
        result = await db.execute(
            text(
                "SELECT * "
                "FROM colocation WHERE id = :id LIMIT 1;"
            ),
            params={"id": request.data.id},
        )
        colocation = result.mappings().first()

        if not colocation:
            return ApiResponse(
                statusCode=404,
                colocation="colocation not found",
                data={"errorcolocation": "no colocation with this id"},
            )

        return ApiResponse(
            statusCode=200,
            colocation="Successfully retrieved colocation",
            data={"colocation": dict(colocation)},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            colocation="Unable to retrieve colocation",
            data={"errorcolocation": str(e)},
        )