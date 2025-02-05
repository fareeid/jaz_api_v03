from datetime import datetime
from typing import Union

from pydantic import BaseModel, ConfigDict


# ########## Installment Schema #########
# Shared properties
class ProposalInstallementBase(BaseModel):
    inst_sr_no: Union[int, None] = None
    inst_curr_code: Union[str | None] = None
    inst_amt: Union[float | None] = None
    inst_due_dt: Union[datetime | None] = None
    paymt_mode: Union[str | None] = None
    paymt_ref: Union[str | None] = None
    paymt_amt: Union[float | None] = None
    paymt_dt: Union[datetime | None] = None


# Properties to receive on Proposal Installment creation
class ProposalInstallmentCreate(ProposalInstallementBase):
    ...


# Properties to receive via API on update by User
class ProposalInstallmentUpdate(ProposalInstallementBase):
    pass


# Properties shared by models stored in DB
class ProposalInstallmentInDBBase(ProposalInstallementBase):
    model_config = ConfigDict(from_attributes=True)

    inst_sys_id: int
    inst_prop_sys_id: int

    # class Config:
    #     from_attributes = True


# Properties to return to client
class ProposalInstallment(ProposalInstallmentInDBBase):
    pass


# Properties stored in DB
class ProposalInstallmentInDB(ProposalInstallmentInDBBase):
    pass
