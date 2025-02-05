from pydantic import ConfigDict

from ..models import PolicyHypothecationBase


class PolicyHypothecationCreate(PolicyHypothecationBase):
    ...


class PolicyHypothecationUpdate(PolicyHypothecationBase):
    ...


class PolicyHypothecationInDBBase(PolicyHypothecationBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class PolicyHypothecation(PolicyHypothecationInDBBase):
    ...


# Properties stored in DB
class PolicyHypothecationInDB(PolicyHypothecationInDBBase):
    ...
