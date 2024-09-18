from typing import Union, Any

from pydantic import BaseModel, ConfigDict


class TypeAttributeBase(BaseModel):
    value: Union[Any, None] = None
    value_code: Union[str, None] = None


class StringAttributeBase(TypeAttributeBase):
    # model_config = ConfigDict(from_attributes=True)
    # entity_id: int
    # attr_sys_id: int
    value: str
    value_code: str


class JsonAttributeBase(TypeAttributeBase):
    value: dict[str, Any]


class AttributeDefinitionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    attr_name: Union[str, None] = None
    data_type: Union[str, None] = None
    entity_type: Union[str, None] = None

    stringattributes: list[StringAttributeBase] = []
