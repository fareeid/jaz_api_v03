from faker import Faker
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas

sample = Faker()


async def sample_user() -> schemas.UserCreateStrict:
    user = schemas.UserCreateStrict(
        first_name=sample.first_name(),
        name=sample.last_name(),
        email=sample.email(),
        username=sample.user_name(),
        phone=sample.phone_number(),
        password="qwerty12345",
        pin="A1234567890D",
    )
    return user


async def create_user(
    async_db: AsyncSession,
    user_in: schemas.UserCreate,
) -> models.User:
    # user_list = await crud.user.get_by_email(async_db, email=user_in.email)
    # if not user_list == []:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="A user with this email already exists in the system",
    #     )
    # user_list = await crud.user.get_by_username(async_db, username=user_in.username)
    # if not user_list == []:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="A user with this username already exists in the system",
    #     )

    user = await crud.user.create(async_db, obj_in=user_in)
    return user


async def get_user(
    async_db: AsyncSession,
    user_in: schemas.UserCreate,
) -> models.User:
    user_list = await crud.user.get_by_all(
        async_db, email=user_in.email, pin=user_in.pin, nic=user_in.nic
    )
    if not user_list == []:
        # if type(user_in) is schemas.UserCreateStrict:
        if isinstance(user_in, schemas.UserCreateStrict):
            raise HTTPException(
                status_code=400,
                detail="A user with these details already exists in the system",
            )
        if len(user_list) > 1:
            user = user_list[0]
            user.id = 0
            return user
            # raise HTTPException(
            #     status_code=400,
            #     detail="Mulitple users found. Contact your admin",
            # )
        user = user_list[0]
    else:
        user = await create_user(async_db, user_in)

    return user
