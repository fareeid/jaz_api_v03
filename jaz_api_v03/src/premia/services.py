from typing import Any, Union

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


def create_policy(non_async_oracle_db: Session, payload_in: premia_models.Policy) -> None:
    """

    @rtype: Policy
    @param non_async_oracle_db:
    @param payload_in:
    @return: Policy
    """
    policy = premia_crud.policy.create_v1(non_async_oracle_db, obj_in=payload_in)
    return policy


def update_policy(non_async_oracle_db: Session, db_obj: premia_models.Policy,
                  payload_in: Union[dict, premia_models.PolicyBase]) -> None:
    policy = premia_crud.policy.update(non_async_oracle_db, db_obj=db_obj, obj_in=payload_in)
    return policy


def get_policy(non_async_oracle_db: Session, policy: premia_models.Policy) -> premia_models.Policy:
    policy = premia_crud.policy.get_policy(non_async_oracle_db, db_obj=policy)
    return policy

def create_receipt_stage(non_async_oracle_db: Session, payload_in: premia_models.ReceiptStagingBase) -> None:
    receipt_stage = premia_crud.receipt_stage.create_v1(non_async_oracle_db, obj_in=payload_in)
    return receipt_stage


def get_cust_code(non_async_oracle_session: Session, cust_in: auth_models.User) -> str:
    cust_code = premia_crud.customer.get_cust_code(non_async_oracle_session, cust_in)
    return cust_code


def create_customer(non_async_oracle_db: Session,
                    premia_cust_payload: premia_models.CustomerBase) -> premia_models.Customer:
    customer = premia_crud.customer.create_v1(nonasync_oracle_db=non_async_oracle_db, obj_in=premia_cust_payload)
    return customer


def get_sys_id(
        non_async_oracle_db: Session, pgi_sequence_name: str) -> int:
    sys_id = premia_crud.policy.get_sys_id(non_async_oracle_db, pgi_sequence_name)
    return sys_id


def get_pol_no(non_async_oracle_db: Session, proposal: dict[str, str]) -> str:
    pol_no = premia_crud.policy.get_pol_no(non_async_oracle_db, proposal)
    return pol_no


def policy_process_json(non_async_oracle_db: Session, pol_trans: premia_models.Policy) -> str:
    pol_no = premia_crud.policy.policy_process_json(non_async_oracle_db, pol_trans)
    return pol_no


def receipt_process_json(non_async_oracle_db: Session, receipt_stage: premia_models.Policy) -> str:
    receipt_num = premia_crud.policy.receipt_process_json(non_async_oracle_db, receipt_stage)
    return receipt_num


def validate_vehicle_json(non_async_oracle_db: Session, search_criteria: dict[str, str]) -> str:
    info = premia_crud.policy.validate_vehicle_json(non_async_oracle_db, search_criteria)
    return info


def calc_premium(non_async_oracle_db: Session, pol_trans: premia_models.Policy) -> str:
    pol_no = premia_crud.policy.calc_premium(non_async_oracle_db, pol_trans)
    return pol_no
