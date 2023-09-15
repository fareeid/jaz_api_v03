from typing import Union

from pydantic import UUID4, BaseModel


class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class PersonBase(BaseModel):
    email: str


class PersonCreate(PersonBase):
    hashed_password: str


# password_regex = "((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,64})"
# class User(BaseModel):
#    password: str = Field(..., regex=password_regex)


class Person(PersonBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        from_attributes = True


# Testing async with model validation
class NoteBase(BaseModel):
    text: str
    completed: bool


class NoteIn(NoteBase):
    pass


class Note(NoteBase):
    id: int

    class Config:
        from_attributes = True


# https://github.com/fareeid/fastapi-simple-app-example/tree/part-3
# Shared properties
class PostBase(BaseModel):
    title: Union[str, None] = None
    body: Union[str, None] = None


# Properties to receive via API on creation
class PostCreate(PostBase):
    title: str
    body: str


# Properties to receive via API on update
class PostUpdate(PostBase):
    pass


class PostInDBBase(PostBase):
    id: Union[UUID4, None] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Post(PostInDBBase):
    pass


# Additional properties stored in DB
class PostInDB(PostInDBBase):
    pass
