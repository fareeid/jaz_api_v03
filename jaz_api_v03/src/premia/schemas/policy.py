# from datetime import datetime

from pydantic import ConfigDict

from .policysection import PolicySection
from ..models import PolicyBase


# Properties to receive on Proposal Risk creation
class PolicyCreate(PolicyBase):
    pol_sys_id: int
    pol_end_no_idx: int
    pol_end_sr_no: int
    pol_comp_code: str
    policycurrency_collection: list = []
    policycharge_collection: list = []
    policysection_collection: list = []
    policyhypothecation_collection: list = []


# Properties to receive via API on update by User
class PolicyUpdate(PolicyBase):
    pass


# Properties shared by models stored in DB
class PolicyInDBBase(PolicyBase):
    model_config = ConfigDict(from_attributes=True)

    policysection_collection: list[PolicySection] = []

    # class Config:
    #     from_attributes = True


# Properties to return to client
class Policy(PolicyInDBBase):
    pass


# Properties stored in DB
class PolicyInDB(PolicyInDBBase):
    pass
