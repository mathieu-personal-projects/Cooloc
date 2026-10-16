from pydantic import BaseModel
from uuid import UUID


class TaskGetPayload(BaseModel):
    id: UUID