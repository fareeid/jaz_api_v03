from typing import Union

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    ...


# Properties to receive via API on creation
class UserCreate(UserBase):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    phone: str
    password: str


# Properties to receive via API on update by User
class UserUpdate(UserBase):
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    email: Union[EmailStr | None] = None
    username: Union[str | None] = None
    phone: Union[str | None] = None
    password: Union[str | None] = None
    is_active: Union[bool | None] = True


# Properties to receive via API on update by Staff Admin
class UserUpdateByStaffAdmin(UserBase):
    is_staff: Union[bool | None] = None
    agent_code: Union[str | None] = None


# Properties to receive via API on update by Agency Admin
class UserUpdateByAgencyAdmin(UserBase):
    agent_code: Union[str | None] = None


class UserInDBBase(UserUpdate):
    id: Union[int | None] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass


# Token Schemas
class TokenPayload(BaseModel):
    sub: Union[int | None] = None


class Token(BaseModel):
    access_token: str
    token_type: str
