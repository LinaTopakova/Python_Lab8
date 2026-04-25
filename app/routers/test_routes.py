from fastapi import APIRouter, Request
from app.exceptions import CustomExceptionA, CustomExceptionB

router = APIRouter(prefix="/test", tags=["error tests"])

@router.get("/a/{value}")
async def trigger_a(value: int):
    if value < 0:
        raise CustomExceptionA("Value cannot be negative (CustomA)")
    return {"message": f"OK, value={value}"}

@router.get("/b/{item_id}")
async def trigger_b(item_id: int):
    if item_id > 100:
        raise CustomExceptionB(f"Item {item_id} not found")
    return {"message": f"Item {item_id} exists"}

@router.get("/boom")
async def boom():
    raise RuntimeError("Unexpected internal error")

@router.post("/echo")
async def echo(request: Request):
    return await request.json()

@router.post("/test-mask")
async def test_mask():
    raise RuntimeError("Test masking")