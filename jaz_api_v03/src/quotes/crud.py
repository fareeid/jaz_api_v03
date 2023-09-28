# from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud_base import CRUDBase
from src.quotes.models import Quote
from src.quotes.schemas import QuoteCreate, QuoteUpdate


class CRUDQuote(CRUDBase[Quote, QuoteCreate, QuoteUpdate]):  # type: ignore
    pass


quote = CRUDQuote(Quote)
