from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_session
from ..core.config import Settings, get_settings
from . import schemas, crud_person

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


@router.post("/", response_model=schemas.Person)
async def create_person(
    *,
    async_db: AsyncSession = Depends(get_session),
    person_in: schemas.PersonCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new person.
    """
    user = await crud_person.person.create(async_db, obj_in=person_in)
    return user
