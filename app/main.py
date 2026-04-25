from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.exceptions import CustomExceptionA, CustomExceptionB
from app.handlers import (
    http_exception_handler,
    custom_exception_a_handler,
    custom_exception_b_handler,
    global_exception_handler,
    validation_exception_handler,
)
from app.middleware import RequestIDMiddleware
from app.routers import users_router, test_router

app = FastAPI(title=settings.app_name)

app.add_middleware(RequestIDMiddleware)

app.include_router(users_router)
app.include_router(test_router)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(CustomExceptionA, custom_exception_a_handler)
app.add_exception_handler(CustomExceptionB, custom_exception_b_handler)
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/")
async def root():
    return {"message": "Hello, Error Handling Lab!"}
