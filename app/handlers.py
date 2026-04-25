from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.schemas import ErrorResponse, ProblemDetails, ValidationErrorDetail
from app.logging_config import log_error


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    await log_error(request, exc, exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            error_type="HTTPException",
            message=exc.detail,
            details=None
        ).model_dump()
    )


async def custom_exception_a_handler(request: Request, exc: CustomExceptionA):
    await log_error(request, exc, exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            error_type="CustomAError",
            message=exc.message,
            details=None
        ).model_dump()
    )


async def custom_exception_b_handler(request: Request, exc: CustomExceptionB):
    await log_error(request, exc, exc.status_code)
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            status_code=exc.status_code,
            error_type="CustomBError",
            message=exc.message,
            details=None
        ).model_dump()
    )


async def global_exception_handler(request: Request, exc: Exception):
    await log_error(request, exc, 500)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            status_code=500,
            error_type="InternalServerError",
            message="Internal Server Error",
            details=None
        ).model_dump()
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    await log_error(request, exc, 422)
    errors = []
    for error in exc.errors():
        errors.append(ValidationErrorDetail(
            field=".".join(str(loc) for loc in error["loc"]),
            message=error["msg"],
            code=error["type"]
        ))
    problem = ProblemDetails(
        instance=str(request.url),
        errors=errors if errors else None
    )
    return JSONResponse(
        status_code=422,
        content=problem.model_dump(),
        headers={"Content-Type": "application/problem+json"}
    )
