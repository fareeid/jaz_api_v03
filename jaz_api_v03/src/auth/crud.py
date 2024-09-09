import logging
from typing import Any, Union

from sqlalchemy import select, union
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserUpdate
from .security import get_password_hash, verify_password
from ..db.crud_base import CRUDBase

log = logging.getLogger("uvicorn")


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    async def create(self, async_db: AsyncSession, *, obj_in: UserCreate) -> User:  # type: ignore  # noqa: E501
        user_dict = obj_in.model_dump(exclude_unset=True)
        if user_dict.get("password"):
            user_dict["password"] = get_password_hash(user_dict["password"])
            # del user_dict["password"]
        return await super().create(async_db, obj_in=user_dict)

    async def get_by_email(self, async_db: AsyncSession, email: str) -> list[User]:
        result = await async_db.execute(
            select(self.model).where(self.model.email == email)  # type: ignore
        )
        return list(result.scalars().all())

    async def get_by_pin(self, async_db: AsyncSession, pin: str) -> list[User]:
        result = await async_db.execute(select(self.model).where(self.model.pin == pin))  # type: ignore
        return list(result.scalars().all())

    async def get_by_username(
            self, async_db: AsyncSession, username: str
    ) -> list[User]:
        result = await async_db.execute(
            select(self.model).where(self.model.username == username)  # type: ignore
        )
        return list(result.scalars().all())

    async def get_by_all(
            self,
            async_db: AsyncSession,
            email: Union[str | None] = None,
            # username: Union[str | None] = None,
            pin: Union[str | None] = None,
            nic: Union[str | None] = None,
    ) -> list[Any]:

        # List to store individual queries
        queries = []

        # Check each parameter and create query if not None
        if email:
            # if email is not None or not email:
            queries.append(select(self.model).where(self.model.email == email))  # type: ignore
        # if username is not None:
        #     queries.append(select(self.model).where(self.model.username == username))
        if pin:  # is not None or not pin:
            queries.append(select(self.model).where(self.model.pin == pin))  # type: ignore
        if nic:  # is not None or not nic:
            queries.append(select(self.model).where(self.model.nic == nic))  # type: ignore

        stmt = union(*queries)
        # print(stmt)

        result = await async_db.execute(stmt)

        # user_list = result.all()
        user_model_list = result.mappings().all()
        # print(user_list)
        return user_model_list

    async def authenticate(
            self, async_db: AsyncSession, *, email: str, password: str
    ) -> Union[User | None]:
        user_list: list[User] = await self.get_by_email(async_db, email=email)
        if user_list == []:
            return None
        if not verify_password(password, user_list[0].password):
            return None
        return user_list[0]

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)