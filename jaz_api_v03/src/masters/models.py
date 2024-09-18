from sqlalchemy import ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class Division(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    divn_comp_code: Mapped[str] = mapped_column()
    divn_code: Mapped[str] = mapped_column(index=True)
    divn_name: Mapped[str] = mapped_column(index=True)
    divn_short_name: Mapped[str] = mapped_column(index=True)
    divn_frz_flag: Mapped[bool] = mapped_column()


class Department(Base):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    dept_code: Mapped[str] = mapped_column(index=True)
    dept_name: Mapped[str] = mapped_column(index=True)
    dept_frz_flag: Mapped[bool] = mapped_column()


class UwClass(Base):
    class_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    class_code: Mapped[str] = mapped_column(index=True, nullable=False)
    class_name: Mapped[str] = mapped_column(index=True, nullable=False)
    class_frz_flag: Mapped[bool] = mapped_column()

    # Relation to Product - down
    products: Mapped[list["Product"]] = relationship(
        back_populates="uwclass",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    def __repr__(self) -> str:
        return f"Class(class_code={self.class_code!r}, quot_ref={self.class_name!r})"


class ProductChargeAssociation(Base):
    prod_sys_id: Mapped[int] = mapped_column(ForeignKey("product.prod_sys_id"), primary_key=True)
    chg_sys_id: Mapped[int] = mapped_column(ForeignKey("charge.chg_sys_id"), primary_key=True)


class ProductConditionAssociation(Base):
    prod_sys_id: Mapped[int] = mapped_column(ForeignKey("product.prod_sys_id"), primary_key=True)
    cond_sys_id: Mapped[int] = mapped_column(ForeignKey("condition.cond_sys_id"), primary_key=True)


class ProductSectionAssociation(Base):
    prod_sys_id: Mapped[int] = mapped_column(ForeignKey("product.prod_sys_id"), primary_key=True)
    sec_sys_id: Mapped[int] = mapped_column(ForeignKey("section.sec_sys_id"), primary_key=True)


class Product(Base):
    prod_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prod_code: Mapped[str] = mapped_column(index=True)
    prod_desc: Mapped[str] = mapped_column(index=True)
    prod_frz_flag: Mapped[bool] = mapped_column()

    # Relation to Quote - up
    prod_class_sys_id: Mapped[int] = mapped_column(
        ForeignKey("uwclass.class_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    uwclass: Mapped["UwClass"] = relationship(back_populates="products")

    # Many-to-Many Relation to Charge - down
    charges: Mapped[list["Charge"]] = relationship(secondary="productchargeassociation", back_populates="products")

    # Many-to-Many Relation to Condition - down
    conditions: Mapped[list["Condition"]] = relationship(secondary="productconditionassociation",
                                                         back_populates="products")

    # Many-to-Many Relation to Section - down
    sections: Mapped[list["Section"]] = relationship(secondary="productsectionassociation", back_populates="products")


class Charge(Base):
    chg_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chg_code: Mapped[str] = mapped_column(index=True)
    chg_desc: Mapped[str] = mapped_column(index=True)
    chg_annual_rate: Mapped[float] = mapped_column()
    chg_rate_per: Mapped[float] = mapped_column()
    chg_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Product - up
    products: Mapped[list[Product]] = relationship(secondary="productchargeassociation", back_populates="charges")


class Condition(Base):
    cond_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cond_code: Mapped[str] = mapped_column(index=True)
    cond_desc: Mapped[str] = mapped_column(index=True)
    cond_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Product - up
    products: Mapped[list[Product]] = relationship(secondary="productconditionassociation", back_populates="conditions")


class SectionCoverAssociation(Base):
    sec_sys_id: Mapped[int] = mapped_column(ForeignKey("section.sec_sys_id"), primary_key=True)
    cvr_sys_id: Mapped[int] = mapped_column(ForeignKey("cover.cvr_sys_id"), primary_key=True)


class Section(Base):
    sec_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sec_code: Mapped[str] = mapped_column(index=True)
    sec_desc: Mapped[str] = mapped_column(index=True)
    sec_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Product - up
    products: Mapped[list[Product]] = relationship(secondary="productsectionassociation", back_populates="sections")

    # Many-to-Many Relation to Cover - down
    covers: Mapped[list["Cover"]] = relationship(secondary="sectioncoverassociation", back_populates="sections")


class Cover(Base):
    cvr_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cvr_code: Mapped[str] = mapped_column(index=True)
    cvr_desc: Mapped[str] = mapped_column(index=True)
    cvr_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Section - up
    sections: Mapped[list[Section]] = relationship(secondary="sectioncoverassociation", back_populates="covers")


class AttributeDefinition(Base):
    attr_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    attr_name: Mapped[str] = mapped_column(index=True)
    data_type: Mapped[str] = mapped_column(CheckConstraint("data_type IN ('string', 'integer','boolean','list')"))
    entity_type: Mapped[str] = mapped_column(CheckConstraint("entity_type IN ('Product', 'User')"))

    # Relation to StringAttribute - down
    stringattributes: Mapped[list["StringAttribute"]] = relationship(
        back_populates="attributedefinition",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    # Relation to JsonAttribute - down
    jsonattributes: Mapped[list["JsonAttribute"]] = relationship(
        back_populates="attributedefinition",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    # parent_attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"), nullable=True)
    # children_attr: Mapped[list["AttributeDefinition"]] = relationship("AttributeDefinition",
    #                                                                   back_populates="parent_attr")
    # parent_attr: Mapped["AttributeDefinition"] = relationship("AttributeDefinition", remote_side=[attr_sys_id],
    #                                                           back_populates="children_attr")


class StringAttribute(Base):
    str_attr_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entity_type: Mapped[str] = mapped_column(CheckConstraint("entity_type IN ('Product', 'User')"))
    entity_id: Mapped[int] = mapped_column()

    # Relation to AttributeDefinition - up
    attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"))
    attributedefinition: Mapped["AttributeDefinition"] = relationship(back_populates="stringattributes")

    value: Mapped[str] = mapped_column(nullable=True)
    value_code: Mapped[str] = mapped_column(nullable=True)

    parent_str_attr_sys_id: Mapped[int] = mapped_column(ForeignKey("stringattribute.str_attr_sys_id"), nullable=True)
    children_str_attr: Mapped[list["StringAttribute"]] = relationship("StringAttribute",
                                                                      back_populates="parent_str_attr")
    parent_str_attr: Mapped["StringAttribute"] = relationship("StringAttribute", remote_side=[str_attr_sys_id],
                                                              back_populates="children_str_attr")
    __table_args__ = (
        UniqueConstraint('entity_type', 'entity_id', 'attr_sys_id', 'value', 'parent_str_attr_sys_id'),
    )


class JsonAttribute(Base):
    json_attr_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    entity_type: Mapped[str] = mapped_column(CheckConstraint("entity_type IN ('PGIT_POLICY', 'PGIT_POL_SECTION')"))
    entity_id: Mapped[int] = mapped_column()

    # Relation to AttributeDefinition - up
    attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"))
    attributedefinition: Mapped["AttributeDefinition"] = relationship(back_populates="jsonattributes")

    value: Mapped[str] = mapped_column(JSONB, nullable=True)
    value_code: Mapped[str] = mapped_column(nullable=True)

    __table_args__ = (
        UniqueConstraint('entity_type', 'entity_id', 'attr_sys_id'),
    )


class ErrorLog(Base):
    error_log_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    path: Mapped[str] = mapped_column()
    error_log: Mapped[str] = mapped_column()

# data_dict = {
#     "Motor Private": {
#         "Policy Type": [
#             {"value": "Motor Private", "value_code": "1002"},
#             {"value": "Lady Jubilee", "value_code": "1002-01"},
#             {"value": "JUBILEE 24/7", "value_code": "1002-02"},
#             {"value": "Prime Auto", "value_code": "1002-03"}
#         ],
#         "Cover Type": [
#             {"value": "Comprehensive", "value_code": "01"},
#             {"value": "Third Party Only", "value_code": "03"},
#             {"value": "Third Party Fire And Theft", "value_code": "02"}
#         ],
#         "Body Type": [
#             {"value": "SALOON", "value_code": "001"},
#             {"value": "SEDAN", "value_code": "002"},
#             {"value": "VAN", "value_code": "003"},
#             {"value": "DOUBLE CAB", "value_code": "004"},
#             {"value": "HATCHBACK", "value_code": "047"}
#         ]
#     }
# }


# class IntegerAttribute(Base):
#     entity_type: Mapped[str] = mapped_column(CheckConstraint("entity_type IN ('Product', 'User')"), primary_key=True)
#     entity_id: Mapped[int] = mapped_column(primary_key=True)
#     attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"), primary_key=True)
#     attr_value: Mapped[int] = mapped_column(nullable=True)
#
#
# class BooleanAttribute(Base):
#     entity_type: Mapped[str] = mapped_column(CheckConstraint("entity_type IN ('Product', 'User')"), primary_key=True)
#     entity_id: Mapped[int] = mapped_column(primary_key=True)
#     attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"), primary_key=True)
#     attr_value: Mapped[bool] = mapped_column(nullable=True)
#
#
# class DateAttribute(Base):
#     entity_type: Mapped[str] = mapped_column(CheckConstraint("entity_type IN ('Product', 'User')"), primary_key=True)
#     entity_id: Mapped[int] = mapped_column(primary_key=True)
#     attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"), primary_key=True)
#     attr_value: Mapped[datetime] = mapped_column(nullable=True)
#
#
# class Option(Base):
#     option_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
#     attr_sys_id: Mapped[int] = mapped_column(ForeignKey("attributedefinition.attr_sys_id"), nullable=False)
#     value: Mapped[str] = mapped_column(nullable=True)
