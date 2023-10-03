# from sqlalchemy.ext.asyncio import AsyncSession
from src.db.crud_base import CRUDBase
from src.quotes.models import Quote

from . import schemas

# from .schemas import QuoteCreate, QuoteUpdate


class CRUDQuote(CRUDBase[Quote, schemas.QuoteCreate, schemas.QuoteUpdate]):  # type: ignore  # noqa: E501
    pass


quote = CRUDQuote(Quote)
