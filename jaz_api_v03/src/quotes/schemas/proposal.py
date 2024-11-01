from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel, ConfigDict  # , field_serializer

# from . import (  # ProposalCharge,; ProposalChargeCreate,
#     ProposalSection,
#     ProposalSectionCreate,
# )
from .proposalcharge import ProposalCharge, ProposalChargeCreate
from .proposalpremium import ProposalPremium, ProposalPremiumCreate
from .proposalsection import ProposalSection, ProposalSectionCreate


# ########## Proposal Schema #########
# Shared properties
class ProposalBase(BaseModel):
    prop_sr_no: Union[int | None] = None
    prop_paymt_ref: Union[str | None] = None
    prop_paymt_date: Union[datetime | None] = None
    prop_paymt_amt: Union[float | None] = None
    # prop_bank_cust_code: Union[str | None] = None
    # prop_bank_cust_name: Union[str | None] = None
    prop_hypothecation: Union[dict[str, Any] | None] = None
    pol_quot_sys_id: Union[int | None] = None
    pol_quot_no: Union[str | None] = None
    pol_comp_code: Union[str | None] = None
    pol_divn_code: Union[str | None] = None
    pol_dept_code: Union[str | None] = None
    pol_prod_code: Union[str | None] = None
    pol_type: Union[str | None] = None
    pol_cust_code: Union[str | None] = None
    pol_assr_code: Union[str | None] = None
    pol_hypothecation_yn: Union[str | None] = None
    pol_fm_dt: Union[datetime | None] = None
    pol_to_dt: Union[datetime | None] = None
    pol_dflt_si_curr_code: Union[str | None] = None
    pol_prem_curr_code: Union[str | None] = None
    pol_flexi: Union[dict[str, Any] | None] = None
    pol_prop_sys_id: Union[int | None] = None

    # @field_serializer("pol_fm_dt", "pol_to_dt")  # type: ignore
    # def serialize_dt(self, dt: datetime, _info: str):
    #     return dt.strftime("%d-%b-%Y %H:%M:%S")


# Properties to receive on Proposal Risk creation
class ProposalCreate(ProposalBase):
    prop_sr_no: int
    pol_comp_code: str
    pol_divn_code: str
    pol_dept_code: str
    pol_prod_code: str
    pol_type: str
    pol_hypothecation_yn: str
    pol_fm_dt: datetime
    pol_to_dt: datetime
    pol_dflt_si_curr_code: str
    pol_prem_curr_code: str
    proposalsections: list[ProposalSectionCreate]
    proposalcharges: list[ProposalChargeCreate]
    proposalpremiums: list[ProposalPremiumCreate] = []
    pol_flexi: dict[str, Any] = {}


# Properties to receive via API on update by User
class ProposalUpdate(ProposalBase):
    pass


# Properties shared by models stored in DB
class ProposalInDBBase(ProposalBase):
    model_config = ConfigDict(from_attributes=True)

    prop_sys_id: int
    prop_quot_sys_id: int
    proposalsections: list[ProposalSection] = []
    proposalcharges: list[ProposalCharge] = []
    proposalpremiums: list[ProposalPremium] = []

    # class Config:
    #     from_attributes = True


# Properties to return to client
class Proposal(ProposalInDBBase):
    pass


# Properties stored in DB
class ProposalInDB(ProposalInDBBase):
    pass
