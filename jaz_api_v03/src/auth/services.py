from faker import Faker
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
