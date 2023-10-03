from typing import Union

from pydantic import BaseModel


# ########## Charge Schema #########
# Shared properties
class ProposalChargeBase(BaseModel):
    chg_sr_no: Union[int | None] = None
    pchg_code: Union[str | None] = None
    pchg_type: Union[str | None] = None
    pchg_perc: Union[float | None] = None
    pchg_chg_fc: Union[float | None] = None
    pchg_prem_curr_code: Union[str | None] = None
    pchg_rate_per: Union[float | None] = None


# Properties to receive on Proposal Charge creation
class ProposalChargeCreate(ProposalChargeBase):
    chg_sr_no: int
    pchg_code: str
    pchg_type: str
    pchg_perc: float
    pchg_chg_fc: float
    pchg_prem_curr_code: str
    pchg_rate_per: float


# Properties to receive via API on update by User
class ProposalChargeUpdate(ProposalChargeBase):
    pass


# Properties shared by models stored in DB
class ProposalChargeInDBBase(ProposalChargeBase):
    chg_sys_id: int
    chg_prop_sys_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class ProposalCharge(ProposalChargeInDBBase):
    pass


# Properties properties stored in DB
class ProposalChargeInDB(ProposalChargeInDBBase):
    pass
