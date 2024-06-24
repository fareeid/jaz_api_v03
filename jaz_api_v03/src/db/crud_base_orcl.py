import logging
from typing import Generic, Type, TypeVar

# from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

# from sqlalchemy import delete, select
# from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401
from sqlalchemy.orm import Session

from ..premia.models import OrclBase

# Define custom types for SQLAlchemy model, and Pydantic schemas
ModelType = TypeVar("ModelType", bound=OrclBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

log = logging.getLogger("uvicorn")


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        Base class that can be extend by other action classes.

        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model

    def create_v1(self, oracle_db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        # print(obj_in)
        db_obj = self.model(**obj_in)
        oracle_db.add(db_obj)
        oracle_db.commit()
        oracle_db.refresh(db_obj)
        return db_obj
