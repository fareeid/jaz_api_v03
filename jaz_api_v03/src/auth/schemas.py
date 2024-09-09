from datetime import datetime
from typing import Union, Any

from pydantic import BaseModel, EmailStr, ConfigDict, model_validator


# Shared properties
class UserBase(BaseModel):
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    name: Union[str | None] = None
    username: Union[str | None] = None
    password: Union[str | None] = None
    email: Union[EmailStr | None] = None
    phone: Union[str | None] = None
    nic: Union[str | None] = None
    pin: Union[str | None] = None
    lic_no: Union[str | None] = None
    gender: Union[str | None] = None
    dob: Union[datetime | None] = None
    is_staff: Union[bool | None] = False
    user_flexi: Union[dict[str, Any] | None] = None
    cust_code: Union[str | None] = None
    cust_cc_code: Union[str | None] = None
    cust_customer_type: Union[str | None] = None
    premia_cust_payload: Union[dict[str, Any] | None] = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    first_name: str
    pin: str
    email: EmailStr

    @model_validator(mode="before")
    @classmethod
    def create_cust_payload(cls, values: dict):
        nic = values.get("nic")
        lic_no = values.get("lic_no")
        if nic and not lic_no:
            values["cust_customer_type"] = "02"
            values["cust_cc_code"] = "01"
        if lic_no and not nic:
            values["cust_customer_type"] = "01"
            values["cust_cc_code"] = "10"

        cust_payload = {
            "cust_first_name": (values.get("first_name") or values.get("name")).upper(),
            "cust_last_name": (values.get("last_name") or "").upper(),
            "cust_name": values.get("name").upper(),
            "cust_email1": values.get("email"),
            "cust_mobile_no": values.get("phone"),
            "cust_civil_id": values.get("pin"),
            "cust_ref_no": values.get("nic"),
            "cust_gender": values.get("gender"),
            "cust_dob": values.get("dob"),
            "cust_customer_type": values.get("cust_customer_type"),
            "cust_cc_code": values.get("cust_cc_code"),
        }
        if values.get("cust_cc_code") == "01":
            cust_payload["cust_cc_prefix"] = "K01"
        if values.get("cust_cc_code") == "10":
            cust_payload["cust_cc_prefix"] = "K10"

        cust_payload["cust_mast_def_code"] = "DIRCL"
        cust_payload["cust_mc_code"] = "01"
        cust_payload["cust_country"] = "C01"  # Country Code
        cust_payload["cust_flex_03"] = "126"  # Country of Birth
        cust_payload["cust_flex_04"] = "126"  # Country of residence
        cust_payload["cust_dflt_assr_yn"] = "1"
        cust_payload["cust_all_curr_appl_yn"] = "1"
        cust_payload["cust_tax_yn"] = "1"
        cust_payload["cust_vat_yn"] = "1"
        cust_payload["cust_wht_yn"] = "1"
        cust_payload["cust_cc_type"] = "001"

        values["premia_cust_payload"] = cust_payload

        return values

# Properties to receive via API on creation
class UserCreateStrict(UserCreate):
    last_name: str
    phone: str
    password: str

    @model_validator(mode="before")
    @classmethod
    def validate_customer_type(cls, values: dict):
        nic = values.get("nic")
        lic_no = values.get("lic_no")
        if nic and lic_no:
            raise ValueError("National ID and License No are mutually exclusive")
        if not nic and not lic_no:
            raise ValueError("You must provide either a National ID No. or Corporate License No. but not both")

        return values

    # @model_validator(mode="after")
    # @classmethod
    # def create_premia_cust_payload(cls, values: dict):
    #     pass
    #     return values

    # @model_validator(mode="before")
    # def validate_corporate(cls, values: dict):
    #     is_corporate = values.get("is_corporate")
    #     if is_corporate:
    #         if not values.get("lic_no"):
    #             raise ValueError("Corporate license is missing")
    #         if values.get("nic"):
    #             raise ValueError("National ID no must be blank for Corporates")
    #     else:
    #         if values.get("lic_no"):
    #             raise ValueError("License No must be blank for Individuals")
    #         if not values.get("nic"):
    #             raise ValueError("National ID is missing")
    #     return values


# Properties to receive via API on update by User
class UserUpdate(BaseModel):
    password: Union[str | None] = None
    is_active: Union[bool | None] = True


# Properties to receive via API on update by Staff Admin
class UserUpdateByStaffAdmin(BaseModel):
    is_staff: Union[bool | None] = None
    agent_code: Union[str | None] = None


# Properties to receive via API on update by Agency Admin
class UserUpdateByAgencyAdmin(BaseModel):
    agent_code: Union[str | None] = None


class UserInDBBase(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: Union[int | None] = None

    # class Config:
    #     from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass


# Token Schemas
class TokenPayload(BaseModel):
    sub: Union[int | None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
