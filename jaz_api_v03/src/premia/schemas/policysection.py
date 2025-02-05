from pydantic import ConfigDict

from ..models import PolicySectionBase


class PolicySectionCreate(PolicySectionBase):
    policyrisk_collection: list = []


class PolicySectionUpdate(PolicySectionBase):
    ...


class PolicySectionInDBBase(PolicySectionBase):
    model_config = ConfigDict(from_attributes=True)


# Properties to return to client
class PolicySection(PolicySectionInDBBase):
    ...


# Properties stored in DB
class PolicySectionInDB(PolicySectionInDBBase):
    ...
