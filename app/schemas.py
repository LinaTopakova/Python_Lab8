import re
from pydantic import BaseModel, EmailStr, constr, conint, Field, field_validator
from typing import Any, List, Optional


class ErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    details: Optional[Any] = None


class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one digit')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


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
