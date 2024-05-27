import logging
from typing import Any, Generic, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base

log = logging.getLogger("uvicorn")

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        Base class that can be extend by other action classes.

        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model

    async def create_v1(
        self, async_db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        print(obj_in)
        db_obj = self.model(**obj_in)
        async_db.add(db_obj)
        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

    async def create(
        self, async_db: AsyncSession, *, obj_in: Union[CreateSchemaType, dict[str, Any]]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            # insert_data = jsonable_encoder(obj_in, exclude_unset=True)
            insert_data = obj_in
        else:
            insert_data = obj_in.dict(exclude_unset=True)
        print(jsonable_encoder(insert_data))
        db_obj = self.model(**insert_data)
        async_db.add(db_obj)
        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

    async def create_v2(
        self, async_db: AsyncSession, *, obj_in: dict[str, Any]
    ) -> ModelType:
        db_obj = self.model(**obj_in)
        async_db.add(db_obj)
        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        async_db: AsyncSession,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        async_db.add(db_obj)

        await async_db.commit()
        await async_db.refresh(db_obj)
        return db_obj

    async def get(self, async_db: AsyncSession, id: int) -> list[ModelType]:
        result = await async_db.execute(select(self.model).where(self.model.id == id))
        return list(result.scalars().all())

    async def get_multi(
        self, async_db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[ModelType]:
        result = await async_db.execute(select(self.model).offset(skip).limit(limit))
        return list(result.scalars().all())

    async def remove(self, async_db: AsyncSession, *, id: int) -> ModelType:
        obj = await async_db.execute(select(self.model).where(self.model.id == id))
        deleted_obj = list(obj.scalars().all())[0]
        await async_db.execute(delete(self.model).where(self.model.id == id))
        await async_db.commit()
        return deleted_obj
