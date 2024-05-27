from typing import Union

from pydantic import BaseModel


class QuoteMarineBase(BaseModel):
    Reference: Union[str | None] = None
    MCI_PaymentStatus: Union[str | None] = None
    MCI_MPESAReference: Union[str | None] = None
    MCI_MPESAAmount: Union[str | None] = None
    MCI_MPESAPayDate: Union[str | None] = None
    MCI_IRAPolicyNum: Union[str | None] = None
    MCI_Cargo_ImporterName: Union[str | None] = None
    MCI_Cargo_ImporterAddress: Union[str | None] = None
    MCI_Cargo_ImporterPIN: Union[str | None] = None
    MCI_AccountType: Union[str | None] = None
    MCI_CustomerType: Union[str | None] = None
    MCI_ClearingAgentPIN: Union[str | None] = None
    MCI_ClearingAgentName: Union[str | None] = None
    MCI_CAEmail: Union[str | None] = None
    MCI_InsuranceID: Union[str | None] = None
    MCI_InsuranceName: Union[str | None] = None
    MCI_QuotationAmount: Union[str | None] = None
    MCI_QuotationNumber: Union[str | None] = None
    MCI_QuoteDateTime: Union[str | None] = None
    MCI_QuoteDateExpiry: Union[str | None] = None
    MCI_Cargo_IDF: Union[str | None] = None
    MCI_Cargo_HS_Codes: Union[str | None] = None
    MCI_Cargo_Description: Union[str | None] = None
    MCI_Cargo_invoiceamount: Union[str | None] = None
    MCI_Cargo_Packingmode: Union[str | None] = None
    MCI_Cargo_dischargedate: Union[str | None] = None
    MCI_Cargo_loadingdate: Union[str | None] = None
    MCI_Cargo_originport: Union[str | None] = None
    MCI_Cargo_destinationport: Union[str | None] = None
    MCI_Cargo_transhipmentStatus: Union[str | None] = None
    MCI_Cargo_country_origin: Union[str | None] = None
    MCI_Cargo_country_destination: Union[str | None] = None
    MCI_Cargo_ModeofTransport: Union[str | None] = None
    MCI_Cargo_InsuranceCoverPeriodDays: Union[str | None] = None
    MCI_Vessel_Name: Union[str | None] = None


# Properties to receive on Proposal Risk creation
class QuoteMarineCreate(QuoteMarineBase):
    pass


# Properties to receive via API on update by User
class QuoteMarineUpdate(QuoteMarineBase):
    pass


# Properties shared by models stored in DB
class QuoteMarineInDBBase(QuoteMarineBase):

    class config:
        orm_mode = True


# Properties to return to client
class QuoteMarine(QuoteMarineInDBBase):
    pass


# Properties properties stored in DB
class QuoteMarineInDB(QuoteMarineInDBBase):
    pass
