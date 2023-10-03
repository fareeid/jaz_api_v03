from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import Settings, get_settings
from ..core.dependencies import get_session
from . import crud, dependencies, models, schemas, security

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
    user_list = await crud.user.get_by_email(async_db, email=user_in.email)
    if not user_list == []:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists in the system",
        )
    user_list = await crud.user.get_by_username(async_db, username=user_in.username)
    if not user_list == []:
        raise HTTPException(
            status_code=400,
            detail="A user with this username already exists in the system",
        )

    user = await crud.user.create(async_db, obj_in=user_in)
    return user


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
    async_db: AsyncSession = Depends(get_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await crud.user.authenticate(
        async_db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(
    current_user: models.User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user
