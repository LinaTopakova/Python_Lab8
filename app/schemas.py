from pydantic import BaseModel, EmailStr, constr, conint, Field
from typing import Any, Optional


class ErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    details: Optional[Any] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: conint(gt=18)   # больше 18
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'
