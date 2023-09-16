from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

# from db import Base  # #### Check this. It is disabled by implicit_reexport = True
# from ..db import Base
from ..db.base import Base


class Person(Base):
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)  # type: ignore
    items = relationship(
        "Item", back_populates="owner", lazy="subquery"
    )  # , uselist=False, backref="owner", , lazy="joined"


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("person.id"))

    owner = relationship("Person", back_populates="items")
