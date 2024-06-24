from typing import Any

# from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.dependencies import get_oracle_session, get_oracle_session_sim  # noqa: F401
from ..premia import crud as premia_crud


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


def create_policy() -> None:
    # 1. Check if assured exists
    # 2. Create assured in user table
    # 3.
    ...
