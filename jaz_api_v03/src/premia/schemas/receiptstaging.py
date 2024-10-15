from pydantic import ConfigDict

from ..models import ReceiptStagingBase


class ReceiptStagingCreate(ReceiptStagingBase):
    ...


class ReceiptStagingUpdate(ReceiptStagingBase):
    ...


class ReceiptStagingInDBBase(ReceiptStagingBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class ReceiptStaging(ReceiptStagingInDBBase):
    ...


# Properties stored in DB
class ReceiptStagingInDB(ReceiptStagingInDBBase):
    ...
