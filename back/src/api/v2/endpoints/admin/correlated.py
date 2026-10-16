from collections import defaultdict
from fastapi import APIRouter, Depends, Query
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.auth import require_admin
from src.core.db_connection import get_db
from src.models.api.ApiRequest import ApiRequest
from src.models.api.ApiResponse import ApiResponse
from src.models.payloads.user import UserGetPayload


router = APIRouter(dependencies=[Depends(require_admin)])

USER_COLUMNS = (
    "id, email, first_name, last_name, phone_number, global_role, created_at, updated_at"
)


async def _fetch(db: AsyncSession, sql: str, **params) -> list[dict]:
    result = await db.execute(text(sql), params=params)
    return [dict(row) for row in result.mappings().all()]

def _group_by(rows: list[dict], key: str) -> dict:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    return grouped

async def _attach_related(db: AsyncSession, users: list[dict]) -> list[dict]:
    if not users:
        return []

    ids = [u["id"] for u in users]

    owned = _group_by(
        await _fetch(
            db,
            "SELECT * FROM colocations WHERE owner_id = ANY(:ids) ORDER BY created_at",
            ids=ids,
        ),
        "owner_id",
    )
    memberships = _group_by(
        await _fetch(
            db,
            "SELECT cm.id, cm.user_id, cm.colocation_id, cm.role, cm.joined_at, "
            "       c.title AS colocation_title "
            "FROM colocation_members cm "
            "JOIN colocations c ON c.id = cm.colocation_id "
            "WHERE cm.user_id = ANY(:ids)",
            ids=ids,
        ),
        "user_id",
    )
    applications = _group_by(
        await _fetch(
            db,
            "SELECT a.id, a.applicant_id, a.colocation_id, a.status, a.message, a.created_at, "
            "       c.title AS colocation_title "
            "FROM colocation_applications a "
            "JOIN colocations c ON c.id = a.colocation_id "
            "WHERE a.applicant_id = ANY(:ids) ORDER BY a.created_at DESC",
            ids=ids,
        ),
        "applicant_id",
    )
    tasks = _group_by(
        await _fetch(
            db,
            "SELECT t.*, c.title AS colocation_title "
            "FROM tasks t "
            "JOIN colocations c ON c.id = t.colocation_id "
            "WHERE t.assigned_to_id = ANY(:ids) ORDER BY t.due_date NULLS LAST",
            ids=ids,
        ),
        "assigned_to_id",
    )
    messages = _group_by(
        await _fetch(
            db,
            "SELECT m.*, c.title AS colocation_title "
            "FROM messages m "
            "JOIN colocations c ON c.id = m.colocation_id "
            "WHERE m.sender_id = ANY(:ids) ORDER BY m.created_at",
            ids=ids,
        ),
        "sender_id",
    )

    return [
        {
            **user,
            "owned_colocations": owned.get(user["id"], []),
            # user_id is UNIQUE in colocation_members -> at most one membership
            "membership": (memberships.get(user["id"]) or [None])[0],
            "applications": applications.get(user["id"], []),
            "assigned_tasks": tasks.get(user["id"], []),
            "messages": messages.get(user["id"], []),
        }
        for user in users
    ]


@router.get("/correlated", response_model=ApiResponse[dict])
async def get_all_correlated(limit: int = Query(50, ge=1, le=200), offset: int = Query(0, ge=0), db: AsyncSession = Depends(get_db),) -> ApiResponse[dict]:
    try:
        users = await _fetch(
            db,
            f"SELECT {USER_COLUMNS} FROM users ORDER BY created_at, id "
            "LIMIT :limit OFFSET :offset",
            limit=limit,
            offset=offset,
        )

        return ApiResponse(
            statusCode=200,
            message="Successfully retrieved users with correlated data",
            data={
                "users": await _attach_related(db, users),
                "limit": limit,
                "offset": offset,
            },
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to retrieve correlated data",
            data={"errorMessage": str(e)},
        )


@router.post("/correlated/user", response_model=ApiResponse[dict])
async def get_user_correlated(request: ApiRequest[UserGetPayload],db: AsyncSession = Depends(get_db),) -> ApiResponse[dict]:
    if not request.data:
        return ApiResponse(
            statusCode=400,
            message="Bad request",
            data={"errorMessage": "No data sent"},
        )

    try:
        users = await _fetch(
            db,
            f"SELECT {USER_COLUMNS} FROM users WHERE id = :id LIMIT 1",
            id=request.data.id,
        )

        if not users:
            return ApiResponse(
                statusCode=404,
                message="User not found",
                data={"errorMessage": "no user with this id"},
            )

        [user] = await _attach_related(db, users)

        return ApiResponse(
            statusCode=200,
            message="Successfully retrieved user with correlated data",
            data={"user": user},
        )

    except Exception as e:
        return ApiResponse(
            statusCode=500,
            message="Unable to retrieve correlated data",
            data={"errorMessage": str(e)},
        )