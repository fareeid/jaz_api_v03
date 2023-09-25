from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate
from src.db.crud_base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):  # type: ignore
    async def create(self, async_db: AsyncSession, *, obj_in: UserCreate) -> User:
        user_dict = obj_in.dict(exclude_unset=True)
        return await super().create_v2(async_db, obj_in=user_dict)

    async def get_by_email(self, async_db: AsyncSession, email: str) -> list[User]:  # type: ignore  # noqa: E501
        result = await async_db.execute(
            select(self.model).where(self.model.email == email)
        )
        return list(result.scalars().all())

    async def get_by_username(self, async_db: AsyncSession, username: str) -> list[User]:  # type: ignore  # noqa: E501
        result = await async_db.execute(
            select(self.model).where(self.model.username == username)
        )
        return list(result.scalars().all())


user = CRUDUser(User)
