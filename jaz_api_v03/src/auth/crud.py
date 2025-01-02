import logging
from typing import Any, Union

from sqlalchemy import select, union_all, or_
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate, UserUpdate, UserBase
from .security import get_password_hash, verify_password
from ..core.dependencies import apply_case_insensitive_collation
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
        query = select(self.model).where(
            or_(
                apply_case_insensitive_collation(self.model.username) == username,
                apply_case_insensitive_collation(self.model.email) == username,
                apply_case_insensitive_collation(self.model.phone) == username
            )
        )

        result = await async_db.execute(query)
        # user = result.scalars().first()
        # result = await async_db.execute(
        #     select(self.model).where(self.model.username == username)  # type: ignore
        # )
        return list(result.scalars().all())

    async def get_user_by_all(
            self, async_db: AsyncSession, user_obj: UserBase
    ) -> list[User]:
        """
        Search for a user by email, phone, pin, NIC, and license number.
        All specified conditions must be true for a match.
        """
        # Start with the base query
        query = select(self.model)

        # Extract values from the dictionary
        email = user_obj.email
        phone = user_obj.phone
        pin = user_obj.pin
        nic = user_obj.nic
        lic = user_obj.lic_no

        # Apply filters only for non-None values
        if email:
            query = query.where(apply_case_insensitive_collation(self.model.email) == email)
        if phone:
            query = query.where(apply_case_insensitive_collation(self.model.phone) == phone)
        if pin:
            query = query.where(apply_case_insensitive_collation(self.model.pin) == pin)
        if nic:
            query = query.where(apply_case_insensitive_collation(self.model.nic) == nic)
        elif lic:  # Only include lic if nic is not provided
            query = query.where(apply_case_insensitive_collation(self.model.lic_no) == lic)

        # Execute the query
        result = await async_db.execute(query)
        return list(result.scalars().all())

    async def get_user_by_any(
            self, async_db: AsyncSession, user_obj: UserBase
    ) -> list[User]:
        # Extract values from the dictionary
        email = user_obj.email
        phone = user_obj.phone
        pin = user_obj.pin
        nic = user_obj.nic
        lic = user_obj.lic_no

        """
        Search for a user by email, phone, pin, NIC, or license number.
        If NIC is provided, license number will be ignored.
        """
        # Create dynamic filters
        filters = []
        if email:
            filters.append(self.model.email == email)
        if phone:
            filters.append(self.model.phone == phone)
        if pin:
            filters.append(self.model.pin == pin)
        if nic:
            filters.append(self.model.nic == nic)
        elif lic:  # Only include lic if nic is not provided
            filters.append(self.model.lic_no == lic)

        # Combine filters with OR condition
        result = await async_db.execute(
            select(self.model).where(or_(*filters))  # type: ignore
        )
        return list(result.scalars().all())

    async def get_by_any(
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
            queries.append(
                select(self.model).where(apply_case_insensitive_collation(self.model.email) == email))  # type: ignore
        # if username is not None:
        #     queries.append(select(self.model).where(self.model.username == username))
        if pin:  # is not None or not pin:
            queries.append(
                select(self.model).where(apply_case_insensitive_collation(self.model.pin) == pin))  # type: ignore
        if nic:  # is not None or not nic:
            queries.append(
                select(self.model).where(apply_case_insensitive_collation(self.model.nic) == nic))  # type: ignore

        stmt = union_all(*queries)
        # print(stmt)

        result = await async_db.execute(stmt)

        # user_list = result.all()
        user_model_list = result.mappings().all()
        # print(user_list)
        return user_model_list

    async def get_agent(self, async_db: AsyncSession, search_criteria: dict[str, str]) -> list[User]:
        query = select(self.model)
        # query = self.model.apply_collation(query)
        where_criteria = conditions = [
            apply_case_insensitive_collation(getattr(self.model, attr)) == value
            for attr, value in search_criteria.items()
        ]

        if where_criteria:
            query = query.where(*where_criteria)
            # query = self.model.apply_collation(query)

        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        query_str = str(compiled_query)
        result = await async_db.execute(query)
        agent_list = result.scalars().all()

        return agent_list

    async def authenticate(
            self,
            async_db: AsyncSession,
            *,
            username: str,
            password: str
    ) -> Union[User | None]:
        # user_list: list[User] = await self.get_by_email(async_db, email=email)
        user_list: list[User] = await self.get_by_username(async_db, username=username)
        if not user_list:
            return None
        if not verify_password(password, user_list[0].password):
            return None
        return user_list[0]

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
