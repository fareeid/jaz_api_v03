from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import Settings, get_settings
from ..core.dependencies import get_session
from . import crud, schemas

router = APIRouter()

settings: Settings = get_settings()


@router.post("/open", response_model=schemas.User)  # list[schemas.User]
async def create_user_open(
    *,
    async_db: AsyncSession = Depends(get_session),
    user_in: schemas.UserCreate,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    user = await crud.user.get_by_email(async_db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system",
        )
    user = await crud.user.get_by_username(async_db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists in the system",
        )

    user = await crud.user.create(async_db, obj_in=user_in)
    return user
