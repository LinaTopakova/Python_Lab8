from fastapi import APIRouter

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/error")
async def trigger_error():
    raise ValueError("Test error")
