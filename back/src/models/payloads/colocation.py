from pydantic import BaseModel
from uuid import UUID


class ColocationGetPayload(BaseModel):
    id: UUID