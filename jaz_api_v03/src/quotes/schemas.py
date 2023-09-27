from datetime import datetime
from typing import Union

from pydantic import BaseModel, EmailStr


class PartnerTransItems(BaseModel):
    item_code: str
    type: str  # COOKERS,
    make: str  # ARMCO,
    model: str  # CHEST FREEZER AF-26K,
    serialNumber: str  # 0FYJ4ABH700044V45,
    cost: float  # 30000


class PartnerTransDetails(BaseModel):
    receipt_number: str  # T0008899O0P,
    total_cost: float  # 50000,
    items: list[PartnerTransItems]


# #########Partner Payload#######
class PartnerTransBase(BaseModel):
    partner_id: str  # DIGITAL_MFS_4C939894,
    mfs_transaction_id: str  # 5773197888,
    customer_name: str  # John Doe,
    customer_nic: str  # 3000211,
    customer_pin: str  # P00892519Y,
    customer_mobile: str  # 2547xxxxxxxx,
    customer_email: EmailStr  # test@mfs.co.ke,
    basic_premium: float  # 875,
    policy_num: str  # TXID8000008900,
    policy_start_date: datetime  # 2023-09-26,
    policy_end_date: datetime  # 2024-09-27
    item_details: PartnerTransDetails


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
    # prc_sys_id: Union[int | None] = None
    # prc_sr_no: Union[int | None] = None
    # prc_lvl1_sys_id: Union[int | None] = None
    # prc_pol_sys_id: Union[int | None] = None
    # prc_end_no_idx: Union[int | None] = None


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
class ItemInDB(ProposalCoverInDBBase):
    pass


# ########## Quote Schema #########
# Shared properties
class QuoteBase(BaseModel):
    quote_num: Union[str | None] = None
    quot_paymt_ref: Union[str | None] = None
    quot_paymt_date: Union[datetime | None] = None
    quot_assr_phone: Union[str | None] = None
    quot_assr_email: Union[str | None] = None


# Properties to receive on Proposal Cover creation
class QuoteCreate(QuoteBase):
    quot_num: str
