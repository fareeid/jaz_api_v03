from typing import Any, Union

from pydantic import BaseModel, ConfigDict


# ########## Motor Cert Schema #########
# Shared properties
class ProposalMotorCertBase(BaseModel):
    motor_cert_sr_no: Union[int | None] = None
    prai_risk_sr_no: Union[int, None] = None
    prai_risk_id: Union[str, None] = None
    prai_flexi: Union[dict[str, Any] | None] = None


# Properties to receive on Motor Cert creation
class ProposalMotorCertCreate(ProposalMotorCertBase):
    motor_cert_sr_no: int
    prai_flexi: dict[str, Any] = {}


# Properties to receive via API on update by User
class ProposalMotorCertUpdate(ProposalMotorCertBase):
    pass


# Properties shared by models stored in DB
class ProposalMotorCertInDBBase(ProposalMotorCertBase):
    model_config = ConfigDict(from_attributes=True)

    motor_cert_sys_id: int

    # class Config:
    #     from_attributes = True


# Properties to return to client
class ProposalMotorCert(ProposalMotorCertInDBBase):
    pass


# Properties properties stored in DB
class ProposalMotorCertInDB(ProposalMotorCertInDBBase):
    pass
