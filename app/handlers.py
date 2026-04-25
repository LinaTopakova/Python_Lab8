from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import CustomExceptionA, CustomExceptionB
from app.schemas import ErrorResponse
from app.logging_config import log_error


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
    # Формируем детальные ошибки по полям
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            status_code=422,
            error_type="ValidationError",
            message="Request validation failed",
            details=errors
        ).model_dump()
    )
