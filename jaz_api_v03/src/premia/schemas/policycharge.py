from pydantic import ConfigDict

from ..models import PolicyChargeBase


class PolicyChargeCreate(PolicyChargeBase):
    ...


class PolicyChargeUpdate(PolicyChargeBase):
    ...


class PolicyChargeInDBBase(PolicyChargeBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class PolicyCharge(PolicyChargeInDBBase):
    ...


# Properties stored in DB
class PolicyChargeInDB(PolicyChargeInDBBase):
    ...
