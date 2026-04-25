from pydantic import BaseModel, EmailStr, constr, conint, Field
from typing import Any, List, Optional


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


class ValidationErrorDetail(BaseModel):
    field: str
    message: str
    code: str


class ProblemDetails(BaseModel):
    type: str = "https://example.com/problems/validation-error"
    title: str = "Validation Error"
    status: int = 422
    detail: str = "The request body failed validation."
    instance: str
    errors: Optional[List[ValidationErrorDetail]] = None
