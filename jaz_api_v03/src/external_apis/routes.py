from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud as external_apis_crud, schemas as external_apis_schemas
from ..core.dependencies import get_session

router = APIRouter()


@router.post("/get_payload", response_model=list[external_apis_schemas.ExternalPayloadCreate])  # dict[str, Any]
async def get_payload(
        *,
        async_db: AsyncSession = Depends(get_session),
        reference_in: dict[str, Any],
) -> Any:
    payload = await external_apis_crud.external_payload.get_payload_by_ref(async_db, reference_in)

    if payload is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
        # payload = {"status": "00", "reference": "Transaction not found"}
    # payload = payload.payload
    return payload
