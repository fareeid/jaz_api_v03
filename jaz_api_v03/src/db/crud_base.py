from typing import Generic, Type, TypeVar, Union, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401
from sqlalchemy import select

# from sqlalchemy.orm import Session

from .base import Base

from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

import logging

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

    async def create(
        self, async_db: AsyncSession, *, obj_in: CreateSchemaType
    ) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
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

    async def get(self, async_db: AsyncSession, id: Any) -> Optional[ModelType]:
        result = await async_db.execute(select(self.model).where(self.model.id == id))
        return result.scalars().all()[0]
