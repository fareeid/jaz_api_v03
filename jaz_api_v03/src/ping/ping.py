from typing import Any
from fastapi import APIRouter

router = APIRouter()

@router.get("/ping")
async def pong() -> dict[Any, Any]: 
    return {
        "ping": "pong"
    }