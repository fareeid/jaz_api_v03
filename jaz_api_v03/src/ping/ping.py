from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def pong() -> dict:
    return {
        "ping": "pong"
    }

@router.get("/ping_depracate")
async def pong_azure() -> dict:
    return {
        "ping_depracate": "pong_depracate"
    }
