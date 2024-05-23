from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..db.crud_base_orcl import CRUDBase
from . import models, schemas


class CRUDPolicy(CRUDBase[models.Policy, schemas.PolicyCreate, schemas.PolicyUpdate]):
    def create_v1(
        self, oracle_db: Session, *, obj_in: schemas.PolicyCreate
    ) -> models.Policy:
        policy_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))
        sections_list = obj_in.policysection_collection
        # print(sections_list)
        sections_list_db = [
            models.PolicySection(**section.model_dump(exclude_unset=True))
            for section in sections_list
        ]
        # print(sections_list_db)

        policy_dict = obj_in.model_dump(exclude_unset=True)
        policy_dict["policysection_collection"] = sections_list_db
        return super().create_v1(oracle_db, obj_in=policy_dict)


policy = CRUDPolicy(models.Policy)
