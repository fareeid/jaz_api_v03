from typing import Union

from pydantic import BaseModel, ConfigDict


# ########## Cover Schema #########
# Shared properties
class ProposalCoverBase(BaseModel):
    cvr_sr_no: Union[int | None] = None
    prc_sr_no: Union[int | None] = None
    prc_code: Union[str | None] = None
    prc_rate: Union[float | None] = None
    prc_rate_per: Union[float | None] = None
    prc_si_curr_code: Union[str | None] = None
    prc_prem_curr_code: Union[str | None] = None
    prc_si_fc: Union[float | None] = None
    prc_prem_fc: Union[float | None] = None


# Properties to receive on Proposal Cover creation
class ProposalCoverCreate(ProposalCoverBase):
    cvr_sr_no: int
    prc_code: str
    prc_rate: float
    prc_rate_per: float
    prc_si_curr_code: str
    prc_prem_curr_code: str
    prc_si_fc: float
    prc_prem_fc: float


# Properties to receive via API on update by User
class ProposalCoverUpdate(ProposalCoverBase):
    pass


# Properties shared by models stored in DB
class ProposalCoverInDBBase(ProposalCoverBase):
    model_config = ConfigDict(from_attributes=True)

    cvr_sys_id: int
    cvr_risk_sys_id: int

    # class Config:
    #     from_attributes = True


# Properties to return to client
class ProposalCover(ProposalCoverInDBBase):
    pass


# Properties properties stored in DB
class ProposalCoverInDB(ProposalCoverInDBBase):
    pass
