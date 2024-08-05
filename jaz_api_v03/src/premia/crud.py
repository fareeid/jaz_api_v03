from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models as premia_models, schemas as premia_schemas
from ..auth import schemas as auth_schema, models as auth_models
from ..db.crud_base_orcl import CRUDBase, CreateSchemaType, ModelType


class CRUDPolicy(CRUDBase[premia_models.Policy, premia_schemas.PolicyCreate, premia_schemas.PolicyUpdate]):
    def create_v1(
            self, oracle_db: Session, *, obj_in: premia_schemas.PolicyCreate
    ) -> premia_models.Policy:
        policy_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))
        sections_list = obj_in.policysection_collection
        # print(sections_list)
        sections_list_db = [
            premia_models.PolicySection(**section.model_dump(exclude_unset=True))
            for section in sections_list
        ]
        # print(sections_list_db)

        policy_dict = obj_in.model_dump(exclude_unset=True)
        policy_dict["policysection_collection"] = sections_list_db
        return super().create_v1(oracle_db, obj_in=policy_dict)


class CRUDCustomer(
    CRUDBase[premia_models.Customer, auth_schema.UserCreate, auth_schema.UserUpdate]
):
    def create_v1(self, nonasync_oracle_db: Session, obj_in: CreateSchemaType) -> ModelType:
        return super().create_v1(nonasync_oracle_db, obj_in=obj_in)

    def get_cust_by_pin(self, oracle_db: Session, pin: str) -> list[premia_models.Customer]:
        result = oracle_db.execute(
            select(self.model).where(self.model.cust_civil_id == pin)
        )
        return list(result.scalars().all())

    def get_customer(self, oracle_db: Session, search_criteria: dict[str, str]) -> list[premia_models.Customer]:
        query = select(premia_models.Customer)
        where_criteria = conditions = [getattr(premia_models.Customer, attr) == value for attr, value in
                                       search_criteria.items()]

        if where_criteria:
            query = query.where(*where_criteria)

        compiled_query = query.compile(compile_kwargs={"literal_binds": True})
        query_str = str(compiled_query)
        result = oracle_db.execute(query)
        customer_list = result.scalars().all()

        return customer_list

    def get_cust_code(self, non_async_oracle_db: Session, cust_in: auth_models.User) -> str:
        cust_cc_prefix = cust_in.premia_cust_payload["cust_cc_prefix"]
        query = select(premia_models.DocNumberRange).where(
            premia_models.DocNumberRange.dnr_level_01 == cust_cc_prefix).with_for_update(
            nowait=False, of=premia_models.DocNumberRange.dnr_curr_no)

        result = non_async_oracle_db.execute(query)
        doc_num_rng_obj = result.scalars().all()[0]
        next_no = doc_num_rng_obj.dnr_curr_no + 1
        doc_num_rng_obj = self.update(non_async_oracle_db, db_obj=doc_num_rng_obj, obj_in={"dnr_curr_no": next_no})

        return f"{cust_cc_prefix}{next_no:06}"




policy = CRUDPolicy(premia_models.Policy)
customer = CRUDCustomer(premia_models.Customer)
