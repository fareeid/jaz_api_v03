from typing import Any
from fastapi import APIRouter, Depends

from ..core.config import Settings, get_settings

router = APIRouter()


@router.get("/ping")
async def pong() -> dict[Any, Any]:
    return {"ping": "pong"}


@router.get("/ping_env")
async def pong_env(settings: Settings = Depends(get_settings)) -> dict[Any, Any]:
    return {
        "ping_env": "pong_env",
        "POSTGRES_DB": settings.POSTGRES_DB,
        "environment": settings.SQLALCHEMY_DATABASE_URI,
    }
