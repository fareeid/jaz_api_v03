from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from . import schemas
from .. import models
from ...db.crud_base import CRUDBase


class CRUDQuoteMarine(
    CRUDBase[models.Quote, schemas.QuoteMarineCreate, schemas.QuoteMarineUpdate]
):  # noqa: E501
    async def create_v1(
        self, async_db: AsyncSession, *, obj_in: schemas.QuoteMarineCreate
    ) -> models.Quote:

        marine_dict = jsonable_encoder(obj_in.model_dump(exclude_unset=True))

        data = {
            "quot_payload": marine_dict,
            "quot_ref": marine_dict["Reference"],
        }

        return await super().create_v1(async_db, obj_in=data)  # type: ignore


marine = CRUDQuoteMarine(models.Quote)
