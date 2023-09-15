from uuid import uuid4
from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from ..db import Base  # #### Check this. It is disabled by implicit_reexport = True


class Person(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship(
        "Item", back_populates="owner", lazy="subquery"
    )  # , uselist=False, backref="owner", , lazy="joined"


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("persons.id"))

    owner = relationship("Person", back_populates="items")


class Post(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    title = Column(String)
    body = Column(Text)


class Note(Base):
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    completed = Column(Boolean)

    def __repr__(self) -> str:
        return (
            f"<Note(id='{self.id}', text='{self.text}', completed='{self.completed}')>"
        )
