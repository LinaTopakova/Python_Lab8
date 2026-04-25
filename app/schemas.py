from pydantic import BaseModel
from typing import Any, Optional


class ErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    details: Optional[Any] = None
