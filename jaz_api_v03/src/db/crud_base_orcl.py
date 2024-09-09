import logging
from typing import Generic, Type, TypeVar, Union, Any

from fastapi.encoders import jsonable_encoder
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
        Base class that can be extended by other action classes.

        :param model: The SQLAlchemy model
        :type model: Type[ModelType]
        """
        self.model = model

    def create_v1(self, oracle_db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        # print(obj_in)
        db_obj = self.model(**obj_in)
        oracle_db.add(db_obj)

        # Construct the Insert statement
        # stmt = insert(self.model).values(**obj_in)
        # # Compile the statement with bound parameters
        # compiled_stmt = stmt.compile(dialect=oracle.dialect(), compile_kwargs={"literal_binds": True})
        # sql_statement = str(compiled_stmt)
        # print(sql_statement)  # This will print the SQL with bound parameters

        oracle_db.commit()
        oracle_db.refresh(db_obj)
        return db_obj

    def update(
        self,
        non_async_oracle_db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        non_async_oracle_db.add(db_obj)

        non_async_oracle_db.commit()
        non_async_oracle_db.refresh(db_obj)
        return db_obj