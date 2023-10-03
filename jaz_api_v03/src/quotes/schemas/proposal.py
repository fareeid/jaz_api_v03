from datetime import datetime
from typing import Union

from pydantic import BaseModel

# from . import (  # ProposalCharge,; ProposalChargeCreate,
#     ProposalSection,
#     ProposalSectionCreate,
# )
from .proposalcharge import ProposalCharge, ProposalChargeCreate
from .proposalsection import ProposalSection, ProposalSectionCreate


# ########## Proposal Schema #########
# Shared properties
class ProposalBase(BaseModel):
    prop_sr_no: Union[int | None] = None
    prop_paymt_ref: Union[str | None] = None
    prop_paymt_date: Union[datetime | None] = None
    pol_quot_sys_id: Union[int | None] = None
    pol_quot_no: Union[str | None] = None
    pol_comp_code: Union[str | None] = None
    pol_divn_code: Union[str | None] = None
    pol_prod_code: Union[str | None] = None
    pol_type: Union[str | None] = None
    pol_cust_code: Union[str | None] = None
    pol_assr_code: Union[str | None] = None
    pol_fm_dt: Union[datetime | None] = None
    pol_to_dt: Union[datetime | None] = None
    pol_dflt_si_curr_code: Union[str | None] = None
    pol_prem_curr_code: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class ProposalCreate(ProposalBase):
    prop_sr_no: int
    pol_comp_code: str
    pol_divn_code: str
    pol_prod_code: str
    pol_type: str
    pol_fm_dt: datetime
    pol_to_dt: datetime
    pol_dflt_si_curr_code: str
    pol_prem_curr_code: str
    sections: list[ProposalSectionCreate] = []
    charges: list[ProposalChargeCreate] = []


# Properties to receive via API on update by User
class ProposalUpdate(ProposalBase):
    pass


# Properties shared by models stored in DB
class ProposalInDBBase(ProposalBase):
    prop_sys_id: int
    prop_quot_sys_id: int
    sections: list[ProposalSection] = []
    charges: list[ProposalCharge] = []

    class Config:
        from_attributes = True


# Properties to return to client
class Proposal(ProposalInDBBase):
    pass


# Properties properties stored in DB
class ProposalInDB(ProposalInDBBase):
    pass
