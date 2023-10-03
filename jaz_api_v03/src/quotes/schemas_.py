from datetime import datetime

from pydantic import BaseModel, EmailStr


class PartnerTransItems(BaseModel):
    item_code: str
    item_name: str  # COOKERS,
    item_make: str  # ARMCO,
    item_model: str  # CHEST FREEZER AF-26K,
    item_serial_num: str  # 0FYJ4ABH700044V45,
    item_cost: float  # 30000
    item_prem: float


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
