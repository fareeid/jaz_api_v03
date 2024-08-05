from typing import Union

from pydantic import BaseModel, ConfigDict


class StringAttributeBase(BaseModel):
    # model_config = ConfigDict(from_attributes=True)
    #
    # entity_id: int
    # attr_sys_id: int
    value: str
    value_code: str


class AttributeDefinitionBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    attr_name: Union[str, None] = None
    data_type: Union[str, None] = None
    entity_type: Union[str, None] = None

    stringattributes: list[StringAttributeBase] = []
