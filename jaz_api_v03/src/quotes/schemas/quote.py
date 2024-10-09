from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel, EmailStr, ConfigDict  # , field_serializer

from . import Proposal, ProposalCreate


# ########## Quote Schema #########
# Shared properties
class QuoteBase(BaseModel):
    quot_ref: Union[str | None] = None
    quot_assr_id: Union[int | None] = None
    quot_assr_name: Union[str | None] = None
    quot_assr_nic: Union[str | None] = None
    quot_assr_pin: Union[str | None] = None
    quot_assr_phone: Union[str | None] = None
    quot_assr_email: Union[EmailStr | None] = None
    quot_assr_gender: Union[str | None] = None
    quot_assr_dob: Union[datetime | None] = None
    quot_assr_flexi: Union[dict[str, Any] | None] = None
    quot_paymt_ref: Union[str | None] = None
    quot_paymt_date: Union[datetime | None] = None

    # @field_serializer("quot_paymt_date")  # type: ignore
    # def serialize_dt(self, dt: datetime, _info: str):
    #     return dt.strftime("%d-%b-%Y %H:%M:%S")


# Properties to receive on Proposal Cover creation
class QuoteCreate(QuoteBase):
    quot_ref: str
    proposals: list[ProposalCreate]


# Properties to receive via API on update by User
class QuoteUpdate(QuoteBase):
    pass


# Properties shared by models stored in DB
class QuoteInDBBase(QuoteBase):
    model_config = ConfigDict(from_attributes=True)

    quot_sys_id: int
    proposals: list[Proposal] = []

    # class Config:
    #     from_attributes = True


# Properties to return to client
class Quote(QuoteInDBBase):
    pass


# Properties properties stored in DB
class QuoteInDB(QuoteInDBBase):
    pass
