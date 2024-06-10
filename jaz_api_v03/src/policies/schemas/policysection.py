# from datetime import datetime
from typing import Union

from pydantic import BaseModel


# ########## Policy Schema #########
# Shared properties
class PolicySectionBase(BaseModel):
    psec_sys_id: Union[int | None] = None
    # psec_pol_sys_id: Union[int | None] = None
    # psec_end_no_idx: Union[int | None] = None
    # psec_end_sr_no: Union[int | None] = None
    psec_sec_code: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class PolicySectionCreate(PolicySectionBase):
    psec_sys_id: int
    # psec_pol_sys_id: int
    # psec_end_no_idx: int
    # psec_end_sr_no: int
    psec_sec_code: str


# Properties to receive via API on update by User
class PolicySectionUpdate(PolicySectionBase):
    pass


# Properties shared by models stored in DB
class PolicySectionInDBBase(PolicySectionBase):

    class Config:
        from_attributes = True


# Properties to return to client
class PolicySection(PolicySectionInDBBase):
    pass


# Properties properties stored in DB
class PolicySectionInDB(PolicySectionInDBBase):
    pass
