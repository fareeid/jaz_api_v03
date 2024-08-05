from typing import Any

# from fastapi import Depends
from sqlalchemy.orm import Session

from ..auth import models as auth_models
from ..core.dependencies import get_non_async_oracle_session, get_oracle_session_sim  # noqa: F401
from ..premia import crud as premia_crud, models as premia_models


def get_cust_by_pin(
        # oracle_db: Session = Depends(get_oracle_session),
        oracle_db: Session,
        pin: str,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917")  # noqa: F841
    customer = premia_crud.customer.get_cust_by_pin(oracle_db, pin="A016034508E")
    return customer
    # return {"test_key": "test_value"}


def get_customer(
        oracle_db: Session,
        search_criteria: premia_models.CustomerBase,
) -> list[premia_models.Customer]:
    # customer = customers_crud.get_customer("152917")  # noqa: F841
    customer_list = premia_crud.customer.get_customer(oracle_db, search_criteria=search_criteria)
    return list(customer_list)


def create_policy() -> None:
    # 1. Check if assured exists
    # 2. Create assured in user table
    # 3.
    ...


def get_cust_code(non_async_oracle_session: Session, cust_in: auth_models.User) -> str:
    cust_code = premia_crud.customer.get_cust_code(non_async_oracle_session, cust_in)
    return cust_code


def create_customer(non_async_oracle_db: Session, premia_cust_payload: dict[str, Any]) -> premia_models.Customer:
    customer = premia_crud.customer.create_v1(nonasync_oracle_db=non_async_oracle_db, obj_in=premia_cust_payload)
    return customer
