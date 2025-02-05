from typing import Any, Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas
from ..db.crud_base import CRUDBase, ModelType, UpdateSchemaType


class CRUDExternalPayload(
    CRUDBase[models.ExternalPayload, schemas.ExternalPayloadCreate, schemas.ExternalPayloadUpdate]
):
    async def create_v2(
            self, async_db: AsyncSession, *, obj_in: schemas.ExternalPayloadCreate
    ) -> str:
        return await super().create_v2(async_db, obj_in=obj_in)

    async def update(
            self,
            async_db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, dict[str, Any]]
    ) -> ModelType:
        payload_out = await super().update(async_db, db_obj=db_obj, obj_in=obj_in)  # obj_in={"is_active": True}
        return payload_out

    async def get_payload_by_ref(self, async_db: AsyncSession, reference_in: dict[str, Any]) -> models.ExternalPayload:
        key, value = next(iter(reference_in.items()))
        stmt = select(models.ExternalPayload).where(models.ExternalPayload.payload[key].astext == value)
        result = await async_db.execute(stmt)
        return result.scalars().all()


external_payload = CRUDExternalPayload(models.ExternalPayload)
