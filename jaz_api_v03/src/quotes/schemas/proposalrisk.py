from typing import Any, Union

from pydantic import BaseModel, ConfigDict

# from . import ProposalCover, ProposalCoverCreate, ProposalSMI, ProposalSMICreate
from .proposalcover import ProposalCover, ProposalCoverCreate
from .proposalmotorcert import ProposalMotorCertCreate
from .proposalsmi import ProposalSMI, ProposalSMICreate


class PraiFlexi(BaseModel):
    prai_data_18: Union[str | None] = None
    prai_code_03: Union[str | None] = None
    prai_desc_09: Union[str | None] = None


# ########## Risk Schema #########
# Shared properties
class ProposalRiskBase(BaseModel):
    risk_sr_no: Union[int, None] = None
    prai_risk_sr_no: Union[int, None] = None
    prai_risk_id: Union[str, None] = None
    prai_flexi: Union[dict[str, Any], None] = None


# Properties to receive on Proposal Risk creation
class ProposalRiskCreate(ProposalRiskBase):
    risk_sr_no: int
    proposalcovers: list[ProposalCoverCreate]
    proposalsmis: list[ProposalSMICreate] = []
    prai_flexi: dict[str, Any] = {}
    proposalmotorcerts: list[ProposalMotorCertCreate] = []


# Properties to receive via API on update by User
class ProposalRiskUpdate(ProposalRiskBase):
    pass


# Properties shared by models stored in DB
class ProposalRiskInDBBase(ProposalRiskBase):
    model_config = ConfigDict(from_attributes=True)

    risk_sys_id: int
    risk_sec_sys_id: int
    proposalcovers: list[ProposalCover] = []
    proposalsmis: list[ProposalSMI] = []

    # class Config:
    #     from_attributes = True


# Properties to return to client
class ProposalRisk(ProposalRiskInDBBase):
    pass


# Properties properties stored in DB
class ProposalRiskInDB(ProposalRiskInDBBase):
    pass
    pass
