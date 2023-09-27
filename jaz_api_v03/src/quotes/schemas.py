from datetime import datetime
from typing import Union

from pydantic import BaseModel


# ########## Cover Schema #########
# Shared properties
class ProposalCoverBase(BaseModel):
    cvr_sr_no: Union[int | None] = None


# Properties to receive on item update
class ItemUpdate(ProposalCoverBase):
    pass


# ########## Quote Schema #########
# Shared properties
class QuoteBase(BaseModel):
    quote_num: Union[str | None] = None
    quot_paymt_ref: Union[str | None] = None
    quot_paymt_date: Union[datetime | None] = None
    quot_assr_phone: Union[str | None] = None
    quot_assr_email: Union[str | None] = None
