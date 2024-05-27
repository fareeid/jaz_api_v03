from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.crud_base import CRUDBase
from .. import models
from . import schemas


class CRUDQuoteMarine(CRUDBase[models.Quote, schemas.QuoteMarineCreate, schemas.QuoteMarineUpdate]):  # type: ignore  # noqa: E501
    async def create_v1(
        self, async_db: AsyncSession, *, obj_in: schemas.QuoteMarineCreate
    ) -> models.Quote:

        marine_dict = jsonable_encoder(obj_in.dict(exclude_unset=True))

        data = {
            "quot_payload": marine_dict,
            "quot_ref": marine_dict["Reference"],
        }

        return await super().create_v1(async_db, obj_in=data)  # type: ignore


marine = CRUDQuoteMarine(models.Quote)
