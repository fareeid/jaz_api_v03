from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_session
from . import crud, schemas

router = APIRouter()


@router.post("/send_payload", response_model=schemas.Quote)  #  dict[str, Any]
async def send_payload(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # 1. Search and/or create customer details in premia

    # 2. Create quote
    quote_obj = schemas.QuoteCreate(
        quot_ref=payload_in.quote_ref,
        quot_paymt_ref=payload_in.item_details.receipt_number,
        quot_paymt_date=payload_in.policy_start_date,
    )
    quote = await crud.quote.create(async_db, obj_in=quote_obj)

    # 3. create proposal
    # 4. create section
    # 5. Create risk
    # 6. create smi
    # 7. create cover
    # 8. create charges

    # user = await crud.user.get_by_email(async_db, email=payload_in.customer_email)
    # return {"test_key": "test_value"}
    return quote
