from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_session
from . import schemas

router = APIRouter()


@router.post("/send_payload", response_model=dict[str, Any])  # schemas.Person
async def send_payload(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Search for customer details in premia
    """
    # user = await crud.user.get_by_email(async_db, email=payload_in.customer_email)

    # user_data =
    # person = await crud_person.person.create(async_db, obj_in=person_in)
    return {"test_key": "test_value"}
