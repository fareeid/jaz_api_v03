from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text  # Column, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..core.dependencies import get_oracle_session, get_session
from . import crud, schemas, schemas_

router = APIRouter()


@router.post("/send_payload", response_model=schemas.Quote)  # dict[str, Any]
async def send_payload(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # 1. Search and/or create customer details in premia

    # 2. create proposal cover
    # proposal_cover_obj = schemas.ProposalCoverCreate(
    #     cvr_sr_no=1,
    #     prc_code="3553",
    #     prc_rate=1.75,
    #     prc_rate_per=1000,
    #     prc_si_curr_code="KES",
    #     prc_prem_curr_code="KES",
    #     prc_si_fc=payload_in.items_total_cost,
    #     prc_prem_fc=payload_in.premium.basic_prem,
    # )

    # 3. create proposal smi
    items = payload_in.items
    for item in enumerate(items, 1):
        sr_no, smi = item

    # proposal_smi_obj = schemas.ProposalSMICreate(smi_sr_no=1)

    # 8. Create quote
    quote_obj = schemas.QuoteCreate(
        quot_ref=payload_in.trans_ref,
        quot_paymt_ref=payload_in.prem_payment_ref,
        quot_paymt_date=payload_in.prem_payment_date,
    )
    quote = await crud.quote.create(async_db, obj_in=quote_obj)

    # 3. create proposal
    # 4. create section
    # 5. Create risk

    # 7. create cover
    # 8. create charges

    # user = await crud.user.get_by_email(async_db, email=payload_in.customer_email)
    # return {"test_key": "test_value"}
    return quote


@router.post("/test_ora_conn")  # dict[str, Any] , response_model=schemas.Quote
def test_oracle(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    result = oracle_db.execute(text("select * from jick_t where rownum<=5"))
    return result.scalars().all()
    # list(result.scalars().all())
