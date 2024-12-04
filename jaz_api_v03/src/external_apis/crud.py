from typing import Any

from sqlalchemy import select
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

    async def get_payload_by_ref(self, async_db: AsyncSession, reference_in: dict[str, Any]) -> models.ExternalPayload:
        key, value = next(iter(reference_in.items()))
        stmt = select(models.ExternalPayload).where(models.ExternalPayload.payload[key].astext == value)
        result = await async_db.execute(stmt)
        return result.scalars().first()



external_payload = CRUDExternalPayload(models.ExternalPayload)