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
    is_active = Column(Boolean(), default=True)  # type: ignore
    is_superuser = Column(Boolean(), default=False)  # type: ignore
    items = relationship(
        "Item",
        back_populates="owner",
        lazy="subquery",
        cascade="all, delete",
        passive_deletes=True,
    )  # , uselist=False, backref="owner", , lazy="joined"


class Item(Base):
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(
        Integer, ForeignKey("person.id", ondelete="CASCADE", onupdate="CASCADE")
    )

    owner = relationship(
        "Person",
        back_populates="items",
    )


# # Modify your tags relationship to the following:
# class Post(db.Model):
#     ...
#     tags = db.relationship(
#         "Tag",
#         secondary="post_tags",
#         back_populates="posts",  # use back-populates instead of backref
#         cascade="all, delete",
#     )


# # Also, define your relationship from your tag model
# class Tag(db.Model):
#     __tablename__ = "tags"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String, unique=True)
#     posts = db.relationship(
#         "Post",
#         secondary="post_tags",
#         back_populates="tags",  # use back-populates instead of backref
#         # When a parent ("post") is deleted, don't delete the tags...
#         passive_deletes=True,
#     )
