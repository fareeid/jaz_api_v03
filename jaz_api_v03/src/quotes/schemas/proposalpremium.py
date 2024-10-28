from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict

from .proposalinstallment import ProposalInstallment, ProposalInstallmentCreate


# ########## Premium Schema #########
# Shared properties
class ProposalPremiumBase(BaseModel):
    prem_sr_no: Union[int, None] = None
    prem_tot_amt: Union[float, None] = None
    prem_curr_code: Union[str, None] = None
    ad_pol_sys_id: Union[int, None] = None
    ad_end_no_idx: Union[int, None] = None
    ad_pol_no: Union[str, None] = None
    ad_end_no: Union[str, None] = None
    ad_doc_dt: Union[datetime, None] = None
    ad_tran_code_doc_no: Union[str, None] = None
    ad_premium: Union[float, None] = None
    ad_stamp_duty: Union[float, None] = None
    ad_pcf: Union[float, None] = None
    ad_itl: Union[float, None] = None
    ad_comesa_fee: Union[float, None] = None
    ad_road_rescue: Union[float, None] = None
    ad_commission: Union[float, None] = None
    ad_wht: Union[float, None] = None


# Properties to receive on Proposal Premium creation
class ProposalPremiumCreate(ProposalPremiumBase):
    proposalinstallments: list[ProposalInstallmentCreate] = []


# Properties to receive via API on update by User
class ProposalPremiumUpdate(ProposalPremiumBase):
    pass


# Properties shared by models stored in DB
class ProposalPremiumInDBBase(ProposalPremiumBase):
    model_config = ConfigDict(from_attributes=True)

    inst_sys_id: int
    inst_prop_sys_id: int
    proposalinstallments: list[ProposalInstallment] = []

    # class Config:
    #     from_attributes = True


# Properties to return to client
class ProposalPremium(ProposalPremiumInDBBase):
    pass


# Properties stored in DB
class ProposalPremiumInDB(ProposalPremiumInDBBase):
    pass
