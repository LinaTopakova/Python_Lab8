from fastapi import APIRouter, HTTPException, status

from app.schemas import UserCreate, ProblemDetails

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/register",
    responses={
        422: {
            "description": "Validation Error",
            "content": {
                "application/problem+json": {
                    "schema": ProblemDetails.model_json_schema(),
                    "example": {
                        "type": "https://example.com/problems/validation-error",
                        "title": "Validation Error",
                        "status": 422,
                        "detail": "The request body failed validation.",
                        "instance": "/users/register",
                        "errors": [
                            {"field": "age", "message": "ensure this value is greater than 18", "code": "value_error.number.not_gt"},
                            {"field": "email", "message": "value is not a valid email address", "code": "value_error.email"}
                        ]
                    }
                }
            }
        }
    }
)
async def register(user: UserCreate):
    return {"username": user.username, "email": user.email}
