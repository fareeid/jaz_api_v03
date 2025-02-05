from pydantic import ConfigDict

from ..models import PolicyRiskBase


class PolicyRiskCreate(PolicyRiskBase):
    policycover_collection: list = []


class PolicyRiskUpdate(PolicyRiskBase):
    ...


class PolicyRiskInDBBase(PolicyRiskBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class PolicyRisk(PolicyRiskInDBBase):
    ...


# Properties stored in DB
class PolicyRiskInDB(PolicyRiskInDBBase):
    ...
