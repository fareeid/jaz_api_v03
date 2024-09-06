from typing import Union, Any

from pydantic import BaseModel


class ExternalPayloadBase(BaseModel):
    external_party: Union[str, None] = None
    transaction_type: Union[str, None] = None
    notification: Union[str, None] = None
    payload: Union[dict[str, Any], None] = None


class ExternalPayloadCreate(ExternalPayloadBase):
    external_party: str
    transaction_type: str
    notification: str


class ExternalPayloadUpdate(ExternalPayloadBase):
    pass
