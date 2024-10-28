import logging
from datetime import datetime
from typing import Generic, Type, TypeVar, Union, Any

from dateutil import parser
from fastapi.encoders import jsonable_encoder
# from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import insert
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

    def is_date(self, value: str) -> bool:
        try:
            datetime.strptime(value, '%Y-%m-%d %H:%M')
            return True
        except ValueError:
            return False

    def parse_datetime(self, date_string: str, default: Union[datetime | None] = None) -> Any:
        try:
            return parser.parse(date_string, dayfirst=True)
        except (ValueError, TypeError):
            return default

    def create_v1(self, oracle_db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        # obj_in_data = jsonable_encoder(obj_in)
        # print(obj_in)
        # obj_in_with_date = {}
        # for key, value in obj_in.items():
        #     if key == 'pol_fm_dt' or key == 'pol_to_dt' or key == 'cust_cr_dt':
        #         ...
        #     if isinstance(value, str) and self.is_date(value):
        #         obj_in_data[key] = func.to_date(value, 'YYYY-MM-DD HH24:MI')
        #     else:
        #         obj_in_data[key] = value

        # obj_in_with_date = {**obj_in}
        # obj_in_with_date['cust_cr_dt'] = func.to_date(obj_in_with_date['cust_cr_dt'], 'YYYY-MM-DD HH24:MI')

        # db_obj = self.model(**obj_in_with_date)
        db_obj = self.model(**obj_in)
        oracle_db.add(db_obj)

        # Construct the Insert statement
        stmt = insert(self.model).values(**obj_in)
        # #Compile the statement with bound parameters
        # compiled_stmt = stmt.compile(dialect=oracle.dialect())  #, compile_kwargs={"literal_binds": True}
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

        if hasattr(db_obj, 'pol_sys_id') and hasattr(db_obj, 'pol_end_no_idx') and hasattr(db_obj, 'pol_end_sr_no'):
            primary_key = (db_obj.pol_sys_id, db_obj.pol_end_no_idx, db_obj.pol_end_sr_no)
            refreshed_db_obj = non_async_oracle_db.get(self.model, primary_key)
        else:
            refreshed_db_obj = db_obj

        obj_data = jsonable_encoder(db_obj, exclude_none=True)
        if obj_data is None:
            jsonable_encoder(db_obj, exclude_none=True)
        # obj_data = jsonable_encoder(db_obj, by_alias=True, exclude_unset=True, exclude_defaults=True, exclude=None,
        #                             exclude_none=True)
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

    def get_policy(self,
                   non_async_oracle_db: Session,
                   *,
                   db_obj: ModelType
                   ) -> ModelType:
        primary_key = (db_obj.pol_sys_id, db_obj.pol_end_no_idx, db_obj.pol_end_sr_no)
        refreshed_db_obj = non_async_oracle_db.get(self.model, primary_key)

        # policy = non_async_oracle_db.get(
        #     self.model,  # The model class
        #     primary_key,  # The composite primary key as a tuple
        #     options=[
        #         # Eager load sections -> risks -> covers
        #         joinedload(self.model.sections)
        #         .joinedload(self.model.sections.risks)
        #         .joinedload(Risk.covers),
        #
        #         # Eager load charges related to the policy
        #         joinedload(Policy.charges)
        #     ]
        # )

        return refreshed_db_obj
