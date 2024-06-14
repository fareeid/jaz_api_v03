from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..core.dependencies import get_oracle_session, get_oracle_session_sim  # noqa: F401
from . import crud as policy_crud
from . import schemas

router = APIRouter()


@router.post("/policy", response_model=schemas.Policy)  # dict[str, Any]
def policy(
    *,
    # oracle_db: Session = Depends(get_oracle_session),
    oracle_db: Session = Depends(get_oracle_session_sim),
    payload_in: schemas.PolicyCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917")  # noqa: F841
    policy = policy_crud.policy.create_v1(oracle_db, obj_in=payload_in)
    return policy
    # return {"test_key": "test_value"}
