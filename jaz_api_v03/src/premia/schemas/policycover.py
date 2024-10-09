from pydantic import ConfigDict

from ..models import PolicyCoverBase


class PolicyCoverCreate(PolicyCoverBase):
    ...


class PolicyCoverUpdate(PolicyCoverBase):
    ...


class PolicyCoverInDBBase(PolicyCoverBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class PolicyCover(PolicyCoverInDBBase):
    ...


# Properties stored in DB
class PolicyCoverInDB(PolicyCoverInDBBase):
    ...
