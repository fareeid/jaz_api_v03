from typing import Any, Union

from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud_base import CRUDBase
from src.quotes.models import Quote

from . import schemas

# from .schemas import QuoteCreate, QuoteUpdate


class CRUDQuote(CRUDBase[Quote, schemas.QuoteCreate, schemas.QuoteUpdate]):  # type: ignore  # noqa: E501
    async def create(
        self,
        async_db: AsyncSession,
        *,
        obj_in: Union[schemas.QuoteCreate, dict[str, Any]]
    ) -> Quote:
        quote_dict = obj_in.dict(exclude_unset=True)  # type: ignore
        return await super().create(async_db, obj_in=quote_dict)


quote = CRUDQuote(Quote)
