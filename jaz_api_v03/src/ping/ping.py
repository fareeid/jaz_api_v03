from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def pong() -> dict:
    return {
        "ping": "pong"
    }

@router.get("/ping_azure")
async def pong_azure() -> dict:
    return {
        "ping_azure": "pong_azure"
    }