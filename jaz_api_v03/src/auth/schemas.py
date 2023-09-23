from typing import Union

from pydantic import BaseModel, EmailStr


# Shared properties
class UserBase(BaseModel):
    first_name: Union[str | None] = None
    last_name: Union[str | None] = None
    email: Union[EmailStr | None] = None
    username: Union[str | None] = None
    phone: Union[str | None] = None
    is_active: Union[str | None] = None


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
    password: Union[str | None] = None


# Properties to receive via API on update by Staff Admin
class UserUpdateByStaffAdmin(UserBase):
    is_staff: Union[str | None] = None
    agent_code: Union[str | None] = None


# Properties to receive via API on update by Agency Admin
class UserUpdateByAgencyAdmin(UserBase):
    agent_code: Union[str | None] = None


class UserInDBBase(UserBase):
    id: Union[int | None] = None

    class Config:
        from_attributes = True


# Additional properties to return via API
class User(UserInDBBase):
    pass


# Additional properties stored in DB
class UserInDB(UserInDBBase):
    pass


# class User(Base):
#     id: Mapped[int] = mapped_column(primary_key=True)

#     client_code: Mapped[str] = mapped_column(String(10), nullable=True)
#     agent_code: Mapped[str] = mapped_column(String(10), nullable=True)
#     is_staff: Mapped[bool] = mapped_column(server_default="false")
#     is_active: Mapped[bool] = mapped_column(server_default="false")
#     is_superuser: Mapped[bool] = mapped_column(server_default="false")
# Union[str | None]
