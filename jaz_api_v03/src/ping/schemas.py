from typing import Union

from pydantic import EmailStr, BaseModel  # noqa: F401


class PersonBase(BaseModel):
    email: Union[str | None] = None
    is_active: Union[bool | None] = True
    is_superuser: bool = False
    full_name: Union[str | None] = None


# Properties to receive via API on creation
class PersonCreate(PersonBase):
    email: str
    password: str


# Properties to receive via API on update
class PersonUpdate(PersonBase):
    password: Union[str | None] = None


class PersonInDBBase(PersonBase):
    id: Union[int | None] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class Person(PersonInDBBase):
    pass


# Additional properties stored in DB
class PersonInDB(PersonInDBBase):
    hashed_password: str


# #######################
# Shared properties
class ItemBase(BaseModel):
    title: Union[str | None] = None
    description: Union[str | None] = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    pass


# Properties shared by models stored in DB
class ItemInDBBase(ItemBase):
    id: int
    title: str
    owner_id: int

    class Config:
        from_attributes = True


# Properties to return to client
class Item(ItemInDBBase):
    pass


# Properties properties stored in DB
class ItemInDB(ItemInDBBase):
    pass
