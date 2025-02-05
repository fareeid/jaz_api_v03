# from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict


# ########## Customer Schema #########
# Shared properties
class CustomerBase(BaseModel):
    psec_sys_id: Union[int | None] = None
    # psec_pol_sys_id: Union[int | None] = None
    # psec_end_no_idx: Union[int | None] = None
    # psec_end_sr_no: Union[int | None] = None
    psec_sec_code: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class CustomerCreate(CustomerBase):
    psec_sys_id: int
    # psec_pol_sys_id: int
    # psec_end_no_idx: int
    # psec_end_sr_no: int
    psec_sec_code: str


# Properties to receive via API on update by User
class CustomerUpdate(CustomerBase):
    pass


# Properties shared by models stored in DB
class CustomerInDBBase(CustomerBase):
    model_config = ConfigDict(from_attributes=True)
    # class Config:
    #     from_attributes = True


# Properties to return to client
class Customer(CustomerInDBBase):
    pass


# Properties properties stored in DB
class CustomerInDB(CustomerInDBBase):
    pass
