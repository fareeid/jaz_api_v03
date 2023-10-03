from typing import Union

from pydantic import BaseModel

# from . import ProposalRisk, ProposalRiskCreate
from .proposalrisk import ProposalRisk, ProposalRiskCreate


# ########## Section Schema #########
# Shared properties
class ProposalSectionBase(BaseModel):
    sec_sr_no: Union[int | None] = None
    psec_sec_code: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class ProposalSectionCreate(ProposalSectionBase):
    sec_sr_no: int
    psec_sec_code: str
    risks: list[ProposalRiskCreate] = []


# Properties to receive via API on update by User
class ProposalSectionUpdate(ProposalSectionBase):
    pass


# Properties shared by models stored in DB
class ProposalSectionInDBBase(ProposalSectionBase):
    sec_sys_id: int
    sec_prop_sys_id: int
    risks: list[ProposalRisk] = []

    class Config:
        from_attributes = True


# Properties to return to client
class ProposalSection(ProposalSectionInDBBase):
    pass


# Properties properties stored in DB
class ProposalSectionInDB(ProposalSectionInDBBase):
    pass
