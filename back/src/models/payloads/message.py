from pydantic import BaseModel
from uuid import UUID


class MessageGetPayload(BaseModel):
    id: UUID