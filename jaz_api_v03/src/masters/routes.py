import logging
from typing import Any

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud as attr_crud
from ..core.dependencies import get_session

log = logging.getLogger("uvicorn")

router = APIRouter()


@router.get("/product_lovs/{entity_id}", response_model=dict[Any, Any])
async def get_product_lovs(entity_id: int,
                           async_db: AsyncSession = Depends(get_session),
                           ) -> Any:
    product_lovs = await attr_crud.attrs.get_attrs_lovs(async_db, entity_id)
    return product_lovs


@router.post("/lov/{attr_name}", response_model=dict[Any, Any])
async def get_lov(attr_name: str,
                  async_db: AsyncSession = Depends(get_session),
                  ) -> Any:
    lov = await attr_crud.attrs.get_lov(async_db, attr_name)
    return lov


@router.post("/child_lov", response_model=dict[Any, Any])
async def get_child_lov(
        parent_attr_name: str = Query(..., description="The name of the parent attribute"),
        parent_value: str = Query(..., description="The value of the parent attribute"),
        child_attr_name: str = Query(..., description="The name of the child attribute"),
        async_db: AsyncSession = Depends(get_session),
) -> Any:
    lov = await attr_crud.attrs.get_child_lov(async_db, parent_attr_name, parent_value, child_attr_name)
    return lov
