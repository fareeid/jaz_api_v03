from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class PartnerTransItems(BaseModel):
    item_code: str
    item_name: str  # COOKERS,
    item_make: str  # ARMCO,
    item_model: str  # CHEST FREEZER AF-26K,
    item_serial_num: str  # 0FYJ4ABH700044V45,
    item_cost: float  # 30000


class PartnerTransPremium(BaseModel):
    basic_prem: float  # T0008899O0P,
    pcf: float  # 50000,
    itl: float
    stamp_duty: float
    total: float


# #########Partner Payload#######
class PartnerTransBase(BaseModel):
    cust_code: str  # DIGITAL_MFS_4C939894,
    trans_ref: str  # 5773197888,
    assr_name: str  # John Doe,
    assr_nic: str  # 3000211,
    assr_pin: str  # P00892519Y,
    assr_mobile: str  # 2547xxxxxxxx,
    assr_email: EmailStr  # test@mfs.co.ke,
    start_date: datetime  # "2023-09-26",
    end_date: datetime  # "2024-09-27",
    items_receipt_ref: str  # "T0008899O0P",
    prem_payment_mode: str  # "MPESA",
    prem_payment_ref: str  # "RIS1VW7M7H",
    prem_payment_date: datetime  # "2023-09-26 09:53",
    items_total_cost: float  # 50000,
    items: list[PartnerTransItems]
    premium: PartnerTransPremium


# ########## Cover Schema #########
# Shared properties
class ProposalCoverBase(BaseModel):
    cvr_sr_no: Union[int | None] = None
    prc_code: Union[str | None] = None
    prc_rate: Union[float | None] = None
    prc_rate_per: Union[float | None] = None
    prc_si_curr_code: Union[str | None] = None
    prc_prem_curr_code: Union[str | None] = None
    prc_si_fc: Union[float | None] = None
    prc_prem_fc: Union[float | None] = None


# Properties to receive on Proposal Cover creation
class ProposalCoverCreate(ProposalCoverBase):
    cvr_sr_no: int
    prc_code: str
    prc_rate: float
    prc_rate_per: float
    prc_si_curr_code: str
    prc_prem_curr_code: str
    prc_si_fc: float
    prc_prem_fc: float


# Properties to receive via API on update by User
class ProposalCoverUpdate(ProposalCoverBase):
    pass


# Properties shared by models stored in DB
class ProposalCoverInDBBase(ProposalCoverBase):
    cvr_sys_id: int
    cvr_risk_sys_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class ProposalCover(ProposalCoverInDBBase):
    pass


# Properties properties stored in DB
class ProposalCoverInDB(ProposalCoverInDBBase):
    pass


# ########## SMI Schema #########
# Shared properties
class ProposalSMIBase(BaseModel):
    smi_sr_no: Union[int | None] = None
    prs_smi_code: Union[str | None] = None
    prs_rate: Union[float | None] = None
    prs_rate_per: Union[float | None] = None
    prs_si_fc: Union[float | None] = None
    prs_prem_fc: Union[float | None] = None
    prs_smi_desc: Union[str | None] = None


# Properties to receive on Proposal Cover creation
class ProposalSMICreate(ProposalSMIBase):
    smi_sr_no: int
    prs_smi_code: str
    prs_rate: float
    prs_rate_per: float
    prs_si_fc: float
    prs_prem_fc: float
    prs_smi_desc: str


# Properties to receive via API on update by User
class ProposalSMIUpdate(ProposalSMIBase):
    pass


# Properties shared by models stored in DB
class ProposalSMIInDBBase(ProposalSMIBase):
    smi_sys_id: int
    smi_risk_sys_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class ProposalSMI(ProposalSMIInDBBase):
    pass


# Properties properties stored in DB
class ProposalSMIInDB(ProposalSMIInDBBase):
    pass


# ########## Proposal Schema #########
# Shared properties
class ProposalBase(BaseModel):
    prop_sys_id: Union[int | None] = None
    prop_sr_no: Union[int | None] = None
    prop_paymt_ref: Union[str | None] = None
    prop_paymt_date: Union[datetime | None] = None
    pol_quot_sys_id: Union[int | None] = None
    pol_quot_no: Union[str | None] = None
    pol_comp_code: Union[str | None] = None
    pol_divn_code: Union[str | None] = None
    pol_prod_code: Union[str | None] = None
    pol_type: Union[str | None] = None
    pol_cust_code: Union[str | None] = None
    pol_assr_code: Union[str | None] = None
    pol_fm_dt: Union[datetime | None] = None
    pol_to_dt: Union[datetime | None] = None
    pol_dflt_si_curr_code: Union[str | None] = None
    pol_prem_curr_code: Union[str | None] = None


# ########## Quote Schema #########
# Shared properties
class QuoteBase(BaseModel):
    quot_ref: Union[str | None] = None
    quot_paymt_ref: Union[str | None] = None
    quot_paymt_date: Union[datetime | None] = None
    quot_assr_phone: Union[str | None] = None
    quot_assr_email: Union[str | None] = None


# Properties to receive on Proposal Cover creation
class QuoteCreate(QuoteBase):
    quot_ref: str


# Properties to receive via API on update by User
class QuoteUpdate(QuoteBase):
    pass


# Properties shared by models stored in DB
class QuoteInDBBase(QuoteBase):
    quot_sys_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Quote(QuoteInDBBase):
    pass


# Properties properties stored in DB
class QuoteInDB(QuoteInDBBase):
    pass


"""
{
    "cust_code": "K9999999",
    "trans_ref": "5773197888",
    "assr_name": "John Doe",
    "assr_nic": "3000211",
    "assr_pin": "P00892519Y",
    "assr_mobile": "2547xxxxxxxx",
    "assr_email": "test@mfs.co.ke",
    "start_date": "2023-09-26",
    "end_date": "2024-09-27",
    "items_receipt_ref": "T0008899O0P",
    "prem_payment_mode": "MPESA",
    "prem_payment_ref": "RIS1VW7M7H",
    "prem_payment_date": "2023-09-26 09:53",
    "totalCost": 50000,
    "items": [
        {
            "item_code": "9000004",
            "item_name": "COOKERS",
            "item_make": "ARMCO",
            "item_model": "CHEST FREEZER AF-26K",
            "item_serial_num": "0FYJ4ABH700044V45",
            "item_cost": 30000,
        },
        {
            "item_code": "9000006",
            "item_name": "FREEZERS",
            "item_make": "ARMCO",
            "item_model": "316LTR CHEST FREEZER#BCF3316",
            "item_serial_num": "0FYJ4ABH700044V4005",
            "item_cost": 20000,
        },
    ],
    "premium": {
        "basic_prem": 875,
        "pcf": 12,
        "itl": 11,
        "stamp_duty": 40,
        "total": 1200,
    },
}
"""
