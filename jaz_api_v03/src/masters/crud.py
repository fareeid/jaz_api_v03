from collections import defaultdict
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, selectinload

from . import models as master_models
from .models import ProductChargeAssociation, ProductSectionAssociation, SectionRiskAssociation, RiskCoverAssociation, \
    Section, Risk
from .schemas import attribute as attribute_schema, product as product_schema
from ..db.crud_base import CRUDBase


class CRUDProduct(
    CRUDBase[
        master_models.Product,
        product_schema.ProductBase,
        product_schema.ProductBase
    ]
):
    async def get_product_by_id(
            self, async_db: AsyncSession, *, prod_code: str
    ) -> master_models.Product:
        # stmt = (select(self.model)
        #         .options(
        #     selectinload(self.model.charges).selectinload(ProductChargeAssociation.charge),
        # ).filter(self.model.prod_code == prod_code))
        # compiled_stmt = stmt.compile(compile_kwargs={"literal_binds": True})

        stmt = (select(self.model)
        .where(self.model.prod_code == prod_code)
        .options(
            selectinload(self.model.charges).selectinload(ProductChargeAssociation.charge),
            selectinload(self.model.sections)
            .selectinload(ProductSectionAssociation.section)
            .selectinload(Section.risks)
            .selectinload(SectionRiskAssociation.risk)
            .selectinload(Risk.covers)
            .selectinload(RiskCoverAssociation.cover)
        ))

        # result = await async_db.execute(compiled_stmt)
        result = await async_db.execute(stmt)
        policy_template = result.scalars().first()
        return policy_template


class CRUDAttributeDefinition(
    CRUDBase[
        master_models.AttributeDefinition, attribute_schema.AttributeDefinitionBase, attribute_schema.TypeAttributeBase]
):
    string_attribute_alias = aliased(master_models.StringAttribute)
    json_attribute_alias = aliased(master_models.JsonAttribute)

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
                attribute_schema.StringAttributeBase(value=value, value_code=value_code))

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
            grouped_data[attr_name].append(attribute_schema.StringAttributeBase(value=value, value_code=value_code))

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
            grouped_data[attr_name].append(attribute_schema.StringAttributeBase(value=value, value_code=value_code))

        return grouped_data

    async def get_table_template(self, async_db: AsyncSession, attr_name: str) -> dict[
        str, Any]:  # list[master_models.AttributeDefinition]:
        stmt = (
            select(self.model.attr_name, self.model.data_type, self.model.entity_type, self.json_attribute_alias.value)
            .join(self.json_attribute_alias, self.model.jsonattributes)
            .filter(self.model.attr_name == attr_name)
        )
        result = await async_db.execute(stmt)

        # Fetch the first row, if any
        row = result.fetchone()

        # Return a dictionary if a row is found, otherwise an empty dictionary
        if row:
            attr_name, data_type, entity_type, json_value = row
            return {
                "attr_name": attr_name,
                "data_type": data_type,
                "entity_type": entity_type,
                "json_value": json_value
            }
        return {}


attrs = CRUDAttributeDefinition(master_models.AttributeDefinition)
product = CRUDProduct(master_models.Product)
