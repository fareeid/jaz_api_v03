from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from ..db.crud_base import CRUDBase


class CRUDExternalPayload(
    CRUDBase[models.ExternalPayload, schemas.ExternalPayloadCreate, schemas.ExternalPayloadUpdate]
):
    async def create_v2(
        self, async_db: AsyncSession, *, obj_in: schemas.ExternalPayloadCreate
    ) -> str:
        # payload = jsonable_encoder(obj_in.model_dump(exclude_unset=True))

        return await super().create_v2(async_db, obj_in=obj_in)


external_payload = CRUDExternalPayload(models.ExternalPayload)