from fastapi import APIRouter

from app.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register")
async def register(user: UserCreate):
    return {"username": user.username, "email": user.email}
