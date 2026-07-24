from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel


T = TypeVar("T")

class ApiRequest(BaseModel, Generic[T]):
    Content-Type: str = "application/json"
    csrfToken: str
    jwtToken: Optional[str] = None
    params: Optional[T] = None
    data: Optional[T] = None