import secrets
from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel, Field


T = TypeVar("T")

class ApiRequest(BaseModel, Generic[T]):
    content_type: str = Field(default="application/json", alias="Content-Type")
    csrfToken: str = Field(default_factory=lambda: secrets.token_hex(32))
    jwtToken: Optional[str] = None
    params: Optional[T] = None
    data: Optional[T] = None