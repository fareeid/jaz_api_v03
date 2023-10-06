from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr

from . import Proposal, ProposalCreate


# ########## Quote Schema #########
# Shared properties
class QuoteBase(BaseModel):
    quot_ref: Union[str | None] = None
    quot_paymt_ref: Union[str | None] = None
    quot_paymt_date: Union[datetime | None] = None
    quot_assr_name: Union[str | None] = None
    quot_assr_nic: Union[str | None] = None
    quot_assr_pin: Union[str | None] = None
    quot_assr_phone: Union[str | None] = None
    quot_assr_email: Union[EmailStr | None] = None


# Properties to receive on Proposal Cover creation
class QuoteCreate(QuoteBase):
    quot_ref: str
    proposals: list[ProposalCreate]


# Properties to receive via API on update by User
class QuoteUpdate(QuoteBase):
    pass


# Properties shared by models stored in DB
class QuoteInDBBase(QuoteBase):
    quot_sys_id: int
    proposals: list[Proposal] = []

    class Config:
        from_attributes = True


# Properties to return to client
class Quote(QuoteInDBBase):
    pass


# Properties properties stored in DB
class QuoteInDB(QuoteInDBBase):
    pass
