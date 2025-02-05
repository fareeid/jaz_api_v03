from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .schemas import endt as endt_schemas
from ...core.dependencies import get_session, get_non_async_oracle_session  # Real Premia
from ...premia import schemas as premia_schemas
from ...premia import services as premia_services

router = APIRouter()


@router.post("/endt_init_depr", response_model=dict[str, Any])
async def endt_init_depr(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        endt_init_payload: endt_schemas.EndorsementRequestBase,
        # current_user: user_models.User = Depends(auth_dependencies.get_current_user),
) -> Any:
    pol_sys_id = premia_services.endt_request_depr(non_async_oracle_db, endt_init_payload)
    x = {
        "HEADER": {
            "REQUEST_REF_NO": "1",
            "PROD_CODE": "1002",
            "SEC_CODE": "100201"
        },
        "POLICY_DETAIL": {
            "POLICY_NO": "P/118/1002/2024/000370",
            "ENDORSEMENT_TYPE": "ED002",
            "EFFECTIVE_TO_DATE": "27-SEP-25 00:00",
            "ENDORSEMENT_REMARKS": "Increase of Sum Insured",
            "SECTION_CODE": "100201"
        }
    }

    return x


@router.post("/endt_init", response_model=premia_schemas.PolicyQuerySchema)  # dict[str, Any]
async def endt_init(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        endt_init_payload: endt_schemas.EndtInit,
        # current_user: user_models.User = Depends(auth_dependencies.get_current_user),
) -> Any:
    policy = premia_services.query_policy(non_async_oracle_db, {"pol_no": endt_init_payload.policy_no})

    if policy is None:
        raise HTTPException(status_code=400,
                            detail=f"Policy {endt_init_payload.policy_no} not found")

    if policy[0].pol_appr_sts != "C":
        raise HTTPException(status_code=400,
                            detail=f"There's a pending transaction for policy {endt_init_payload.policy_no}. Please contact support team.")

    if endt_init_payload.endorsement_type == "ED002":
        if endt_init_payload.vehicle_value.prai_num_02 < policy[0].policysection_collection[0].policyrisk_collection[
            0].prai_num_02:
            raise HTTPException(status_code=400,
                                detail=f"Vehicle value cannot be reduced for Increase in SI endorsment.")

    if endt_init_payload.endorsement_type == "ED018":
        if endt_init_payload.vehicle_value.prai_num_02 > policy[0].policysection_collection[0].policyrisk_collection[
            0].prai_num_02:
            raise HTTPException(status_code=400,
                                detail=f"Vehicle value cannot be increased for Decrease in SI endorsment.")

    if endt_init_payload.endorsement_type in ["ED002", "ED018"]:
        if endt_init_payload.vehicle_value.prai_num_02 == policy[0].policysection_collection[0].policyrisk_collection[
            0].prai_num_02:
            raise HTTPException(status_code=400,
                                detail=f"Endorsement has no effect. Please review'")

    endt_status = premia_services.endt_init(non_async_oracle_db, endt_init_payload)
    if not endt_status[0]["STATUS"].startswith("ORA-0000"):
        raise HTTPException(status_code=400,
                            detail=f"Endorsement generated error: {endt_status[0]['STATUS']}. Please contact support team.")

    pol_instance = premia_services.query_policy(non_async_oracle_db, {"pol_no": endt_init_payload.policy_no})
    x = {
        "HEADER": {
            "REQUEST_REF_NO": "1",
            "PROD_CODE": "1002",
            "SEC_CODE": "100201"
        },
        "POLICY_DETAIL": {
            "POLICY_NO": "P/118/1002/2024/000370",
            "ENDORSEMENT_TYPE": "ED002",
            "EFFECTIVE_TO_DATE": "27-SEP-25 00:00",
            "ENDORSEMENT_REMARKS": "Increase of Sum Insured",
            "SECTION_CODE": "100201"
        }
    }

    return pol_instance[0]
