# from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud_base import CRUDBase
from src.quotes.models import Quote
from src.quotes.schemas import QuoteCreate, QuoteUpdate


class CRUDQuote(CRUDBase[Quote, QuoteCreate, QuoteUpdate]):  # type: ignore
    pass

    # async def create(self, async_db: AsyncSession, *, obj_in: QuoteCreate) -> Quote:
    #     quote_dict = obj_in.dict(exclude_unset=True)
    #     return await super().create(async_db, obj_in=quote_dict)


quote = CRUDQuote(Quote)
