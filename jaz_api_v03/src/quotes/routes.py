from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text  # Column, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from ..core.dependencies import get_oracle_session, get_session  # , orcl_base
from ..customer import crud as customers_crud

# from . import crud
from . import crud as quotes_crud
from . import models, schemas, schemas_  # noqa: F401

# from . import schemas, schemas_

router = APIRouter()


@router.post("/quote", response_model=schemas.Quote)  # dict[str, Any]
async def quote(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917")  # noqa: F841
    quote = await quotes_crud.quote.create_v1(async_db, obj_in=payload_in)
    return quote
    # return {"test_key": "test_value"}


@router.post("/quote_cust")  # dict[str, Any] , response_model=schemas.Quote
async def quote_cust(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917x")  # noqa: F841
    # return customer
    policy = customers_crud.get_tables()
    return policy
    # return {"test_key": "test_value"}


@router.post("/test_reflection")  # dict[str, Any] , response_model=schemas.Quote
async def test_reflection(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    proposal_table = customers_crud.get_proposal_table()  # noqa: F841
    # Policy = orcl_base.classes.pgit_policy
    # quote = await quotes_crud.quote.create_v1(async_db, obj_in=payload_in)

    return proposal_table.columns._all_columns
    # return {"test_key": "test_value"}


@router.post("/test_ora_conn")  # dict[str, Any] , response_model=schemas.Quote
def test_oracle(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    result = oracle_db.execute(text("select * from jick_t where rownum<=6"))
    return result.scalars().all()
