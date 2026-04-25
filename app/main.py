from fastapi import FastAPI

from app.config import settings
from app.routers import users_router, test_router

app = FastAPI(title=settings.app_name)

app.include_router(users_router)
app.include_router(test_router)


@app.get("/")
async def root():
    return {"message": "Hello, Error Handling Lab!"}
