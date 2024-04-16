import logging
from typing import Any, Union

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.crud_base import CRUDBase
from .models import Item, Person
from .schemas import PersonCreate, PersonUpdate

log = logging.getLogger("uvicorn")


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):
    async def create(
        self, async_db: AsyncSession, *, obj_in: Union[PersonCreate, dict[str, Any]]
    ) -> Person:
        person_dict = self.replace_pass_items_field(
            obj_in.dict(exclude_unset=True)  # type: ignore
        )  # __dict__
        return await super().create(async_db, obj_in=person_dict)

    async def update(
        self,
        async_db: AsyncSession,
        *,
        db_obj: Person,
        obj_in: Union[PersonUpdate, dict[str, Any]]
    ) -> Person:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        # if update_data["password"]:
        # if update_data.get("password"):
        #     hashed_password = update_data["password"]
        #     del update_data["password"]
        #     update_data["hashed_password"] = hashed_password
        log.info("update_data upstream: " + str(update_data))
        update_dict = self.replace_pass_items_field(update_data)
        return await super().update(async_db, db_obj=db_obj, obj_in=update_dict)

    def replace_pass_items_field(self, obj_in: dict[str, Any]) -> dict[str, Any]:
        """
        Replace password field with hashed_password to make it possible to create a sqlalchemy model Person
        Items contains pydantic model ItemCreate. You need to create sqlalchemy model Item
        """  # noqa: E501
        # if obj_in["password"]:
        if obj_in.get("password"):
            obj_in["hashed_password"] = obj_in["password"]
            del obj_in["password"]
        # if obj_in["items"]:
        if obj_in.get("items"):
            # del obj_in["items"]
            obj_in["items"] = [Item(**item) for item in obj_in["items"]]  # .__dict__
        return obj_in
        # {'email': 'mark64examplenet', 'is_active': True, 'is_superuser': False, 'full_name': 'Edgar Morton', 'password': 'qwerty',   # noqa: E501
        # 'items': [ItemCreate(title='q1', description='zxcv'), ItemCreate(title='q2', description='wqeqee')]}  # noqa: E501


person = CRUDPerson(Person)
