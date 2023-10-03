from typing import Union

from pydantic import BaseModel

# from . import ProposalCover, ProposalCoverCreate, ProposalSMI, ProposalSMICreate
from .proposalcover import ProposalCover, ProposalCoverCreate
from .proposalsmi import ProposalSMI, ProposalSMICreate


# ########## Risk Schema #########
# Shared properties
class ProposalRiskBase(BaseModel):
    risk_sr_no: Union[int | None] = None
    prai_data_18: Union[str | None] = None
    prai_code_03: Union[str | None] = None
    prai_desc_09: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class ProposalRiskCreate(ProposalRiskBase):
    risk_sr_no: int
    prai_data_18: str
    prai_code_03: str
    prai_desc_09: str
    covers: list[ProposalCoverCreate] = []
    smis: list[ProposalSMICreate] = []


# Properties to receive via API on update by User
class ProposalRiskUpdate(ProposalRiskBase):
    pass


# Properties shared by models stored in DB
class ProposalRiskInDBBase(ProposalRiskBase):
    risk_sys_id: int
    risk_sec_sys_id: int
    covers: list[ProposalCover] = []
    smis: list[ProposalSMI] = []

    class Config:
        from_attributes = True


# Properties to return to client
class ProposalRisk(ProposalRiskInDBBase):
    pass


# Properties properties stored in DB
class ProposalRiskInDB(ProposalRiskInDBBase):
    pass
