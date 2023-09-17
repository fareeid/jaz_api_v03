from typing import Union, Any

from src.db.crud_base import CRUDBase
from src.ping.models import Person
from src.ping.schemas import PersonCreate, PersonUpdate

from sqlalchemy.ext.asyncio import AsyncSession


import logging

log = logging.getLogger("uvicorn")


class CRUDPerson(CRUDBase[Person, PersonCreate, PersonUpdate]):  # type: ignore
    async def create(self, async_db: AsyncSession, *, obj_in: PersonCreate) -> Person:
        db_obj = Person(
            email=obj_in.email,
            hashed_password=obj_in.password,
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        async_db.add(db_obj)
        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

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
        if update_data["password"]:
            hashed_password = update_data["password"]
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(async_db, db_obj=db_obj, obj_in=update_data)

    async def createyyyyy(
        self, async_db: AsyncSession, *, obj_in: PersonCreate
    ) -> Person:
        insert_data = obj_in.dict()

        log.info("Test logging from crud_person before...")
        log.info(insert_data)
        if insert_data["password"]:
            hashed_password = insert_data["password"]
            del insert_data["password"]
            insert_data["hashed_password"] = hashed_password
        log.info("Test logging from crud_person after...")
        log.info(insert_data)
        return super().create(async_db, obj_in=insert_data)


person = CRUDPerson(Person)
