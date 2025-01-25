from datetime import datetime

from pydantic import BaseModel, Field


def current_time() -> str:
    """Returns the current date and time in the required format."""
    return datetime.now().strftime("%d-%b-%y %H:%M").upper()


class HeaderBase(BaseModel):
    USERNAME: str = "Jubliee_KE"
    PASSWORD: str = "Azentio@123"
    REQUEST_REF_NO: str
    REQUEST_TIME: str = Field(default_factory=current_time)
    REQUEST_SYSTEM_ID: str = "Jubliee"
    REQUEST_USER_ID: str = "AdminUser"
    SERVICE_TYPE: str = "POLICY"
    PROD_CODE: str
    SEC_CODE: str


class PolicyDetailBase(BaseModel):
    SERVICE_ID: str = "ENDORSEMENT_REQUEST"
    SERVICE_ACTION: str = "I"
    POLICY_NO: str
    ENDORSEMENT_TYPE: str
    EFFECTIVE_FROM_DATE: str = Field(default_factory=current_time)
    EFFECTIVE_TO_DATE: str
    ENDORSEMENT_REMARKS: str = "DefaultRemarks"
    SECTION_CODE: str


class EndorsementRequestBase(BaseModel):
    HEADER: HeaderBase
    POLICY_DETAIL: PolicyDetailBase


class VehicleRegNo(BaseModel):
    prai_data_03: str = Field(..., description="Vehicle registration number")


class VehicleValue(BaseModel):
    prai_num_02: int = Field(..., description="Vehicle value")


class CoverPremium(BaseModel):
    prc_code: str = Field('3101', description="Cover code")
    prc_prem_fc: int = Field(..., description="Premium amount")


class EndtInit(BaseModel):
    request_ref_no: str = Field(..., description="Request reference number")
    request_time: datetime = Field(default_factory=current_time, description="Request timestamp")
    policy_no: str = Field(..., description="Policy number")
    endorsement_type: str = Field(..., description="Endorsement type")
    effective_from_date: datetime = Field(default_factory=current_time, description="Effective from date")
    vehicle_reg_no: VehicleRegNo = Field(None, description="Vehicle registration details")
    vehicle_value: VehicleValue = Field( None, description="Vehicle value details")
    cover_premium: CoverPremium = Field(None, description="Premium details")