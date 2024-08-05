# from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict

from .policysection import PolicySection, PolicySectionCreate


# ########## Policy Schema #########
# Shared properties
class PolicyBase(BaseModel):
    pol_sys_id: Union[int | None] = None
    pol_end_no_idx: Union[int | None] = None
    pol_end_sr_no: Union[int | None] = None
    pol_comp_code: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class PolicyCreate(PolicyBase):
    pol_sys_id: int
    pol_end_no_idx: int
    pol_end_sr_no: int
    pol_comp_code: str
    policysection_collection: list[PolicySectionCreate]


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


# Properties properties stored in DB
class PolicyInDB(PolicyInDBBase):
    pass
