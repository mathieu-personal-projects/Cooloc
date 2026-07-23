from typing import Generic, TypeVar, Optional, Any
from pydantic import BaseModel


T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    statusCode: int = 200
    message: str = "Success"
    data: Optional[T] = None