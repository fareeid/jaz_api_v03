from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from . import models as master_models
from .schemas import product as product_schema
from ..db.crud_base import CRUDBase


class CRUDAttributeDefinition(
    CRUDBase[
        master_models.AttributeDefinition, product_schema.AttributeDefinitionBase, product_schema.StringAttributeBase]
):
    string_attribute_alias = aliased(master_models.StringAttribute)

    async def get_attrs_lovs(self, async_db: AsyncSession, id: int) -> list[master_models.AttributeDefinition]:
        # Aliasing the StringAttribute to avoid any ambiguity in case of multiple joins

        ids = [id, 999]

        stmt = (
            select(
                self.string_attribute_alias.entity_id,
                master_models.AttributeDefinition.attr_name,
                self.string_attribute_alias.value,
                self.string_attribute_alias.value_code)
            .join(self.string_attribute_alias, master_models.AttributeDefinition.stringattributes)
            # .filter(string_attribute_alias.entity_id == id)
            .filter(self.string_attribute_alias.entity_id.in_(ids))
            .filter(master_models.AttributeDefinition.attr_name != "Vehicle Model")
        )

        result = await async_db.execute(stmt)
        rows = result.all()

        # Nested defaultdict to group data by entity_id first, then attr_name
        grouped_data = defaultdict(lambda: defaultdict(list))

        for row in rows:
            entity_id = str(row[0])  # Ensure entity_id is treated as string for dict keys
            attr_name = row[1]
            value = row[2]
            value_code = row[3]
            grouped_data[entity_id][attr_name].append(
                product_schema.StringAttributeBase(value=value, value_code=value_code))

        return dict(grouped_data)

    async def get_child_lov(self, async_db: AsyncSession,
                            parent_attr_name: str,
                            parent_value: str,
                            child_attr_name: str
                            ) -> list[master_models.AttributeDefinition]:

        parent_subquery = (
            select(self.string_attribute_alias.str_attr_sys_id)
            .join(self.string_attribute_alias, master_models.AttributeDefinition.stringattributes)
            .filter(master_models.AttributeDefinition.attr_name.ilike(parent_attr_name))
            .filter(self.string_attribute_alias.value.ilike(parent_value))
            .scalar_subquery()
        )

        stmt = (
            select(master_models.AttributeDefinition.attr_name,
                   self.string_attribute_alias.value,
                   self.string_attribute_alias.value_code)
            .join(self.string_attribute_alias, master_models.AttributeDefinition.stringattributes)
            .filter(master_models.AttributeDefinition.attr_name.ilike(child_attr_name))
            .filter(self.string_attribute_alias.parent_str_attr_sys_id == parent_subquery)
        )

        result = await async_db.execute(stmt)
        rows = result.all()

        grouped_data = defaultdict(list)

        for row in rows:
            attr_name = row[0]
            value = row[1]
            value_code = row[2]
            grouped_data[attr_name].append(product_schema.StringAttributeBase(value=value, value_code=value_code))

        return grouped_data

    async def get_lov(self, async_db: AsyncSession, attr_name: str) -> list[master_models.AttributeDefinition]:
        stmt = (
            select(master_models.AttributeDefinition.attr_name,
                   self.string_attribute_alias.value,
                   self.string_attribute_alias.value_code)
            .join(self.string_attribute_alias, master_models.AttributeDefinition.stringattributes)
            .filter(master_models.AttributeDefinition.attr_name == attr_name)
        )

        result = await async_db.execute(stmt)
        rows = result.all()

        grouped_data = defaultdict(list)

        for row in rows:
            attr_name = row[0]
            value = row[1]
            value_code = row[2]
            grouped_data[attr_name].append(product_schema.StringAttributeBase(value=value, value_code=value_code))

        return grouped_data


attrs = CRUDAttributeDefinition(master_models.AttributeDefinition)
