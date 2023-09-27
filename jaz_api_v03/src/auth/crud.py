import logging
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreate, UserUpdate
from src.db.crud_base import CRUDBase

from .security import get_password_hash, verify_password

log = logging.getLogger("uvicorn")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):  # type: ignore
    async def create(self, async_db: AsyncSession, *, obj_in: UserCreate) -> User:
        user_dict = obj_in.dict(exclude_unset=True)
        if user_dict.get("password"):
            user_dict["password"] = get_password_hash(user_dict["password"])
            # del user_dict["password"]
        return await super().create(async_db, obj_in=user_dict)

    async def get_by_email(self, async_db: AsyncSession, email: str) -> list[User]:
        result = await async_db.execute(
            select(self.model).where(self.model.email == email)
        )
        return list(result.scalars().all())

    async def get_by_username(
        self, async_db: AsyncSession, username: str
    ) -> list[User]:
        result = await async_db.execute(
            select(self.model).where(self.model.username == username)
        )
        return list(result.scalars().all())

    async def authenticate(
        self, async_db: AsyncSession, *, email: str, password: str
    ) -> Union[User | None]:
        user = await self.get_by_email(async_db, email=email)
        if user == []:
            return None
        if not verify_password(password, user[0].password):
            return None
        return user[0]

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
