from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from . import crud as policy_crud, services as premia_services, models as premia_models
# from . import schemas
from ..core.dependencies import get_non_async_oracle_session, get_oracle_session_sim  # noqa: F401

router = APIRouter()


@router.post("/policy", response_model=premia_models.PolicyBase)  # dict[str, Any]
def policy(
        *,
        # oracle_db: Session = Depends(get_oracle_session),
        oracle_db: Session = Depends(get_oracle_session_sim),
        payload_in: premia_models.PolicyBase,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917")  # noqa: F841
    policy = policy_crud.policy.create_v1(oracle_db, obj_in=payload_in)
    return policy
    # return {"test_key": "test_value"}


@router.post("/customer", response_model=list[dict[str, Any]])  # list[premia_models.CustomerBase]
def customer(
        *,
        oracle_db: Session = Depends(get_oracle_session_sim),
        search_criteria: premia_models.CustomerBase,
) -> list[dict[str, Any]]:
    customer_model_list = premia_services.get_customer(oracle_db, search_criteria=search_criteria.model_dump(exclude_unset=True))
    # custtomer_dict_list = [cust.to_dict() for cust in customer_model_list]
    return [cust.to_dict() for cust in customer_model_list]
