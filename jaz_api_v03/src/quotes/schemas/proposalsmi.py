from typing import Union

from pydantic import BaseModel


# ########## SMI Schema #########
# Shared properties
class ProposalSMIBase(BaseModel):
    smi_sr_no: Union[int | None] = None
    prs_smi_code: Union[str | None] = None
    prs_rate: Union[float | None] = None
    prs_rate_per: Union[float | None] = None
    prs_si_fc: Union[float | None] = None
    prs_prem_fc: Union[float | None] = None
    prs_smi_desc: Union[str | None] = None


# Properties to receive on Proposal Cover creation
class ProposalSMICreate(ProposalSMIBase):
    smi_sr_no: int
    prs_smi_code: str
    prs_rate: float
    prs_rate_per: float
    prs_si_fc: float
    prs_prem_fc: float
    prs_smi_desc: str


# Properties to receive via API on update by User
class ProposalSMIUpdate(ProposalSMIBase):
    pass


# Properties shared by models stored in DB
class ProposalSMIInDBBase(ProposalSMIBase):
    smi_sys_id: int
    smi_risk_sys_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class ProposalSMI(ProposalSMIInDBBase):
    pass


# Properties properties stored in DB
class ProposalSMIInDB(ProposalSMIInDBBase):
    pass
    pass
