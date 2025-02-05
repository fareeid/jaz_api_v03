from pydantic import ConfigDict

from ..models import PolicyCurrencyBase


class PolicyCurrencyCreate(PolicyCurrencyBase):
    ...


class PolicyCurrencyUpdate(PolicyCurrencyBase):
    ...


class PolicyCurrencyInDBBase(PolicyCurrencyBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class PolicyCurrency(PolicyCurrencyInDBBase):
    ...


# Properties stored in DB
class PolicyCurrencyInDB(PolicyCurrencyInDBBase):
    ...
