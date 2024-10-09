from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class t__UwClass(Base):
    class_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    class_code: Mapped[str] = mapped_column(index=True, nullable=False)
    class_name: Mapped[str] = mapped_column(index=True, nullable=False)
    class_frz_flag: Mapped[bool] = mapped_column()

    # Relation to Product - down
    t__products: Mapped[list["t__Product"]] = relationship(
        back_populates="t__uwclass",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    def __repr__(self) -> str:
        return f"Class(class_code={self.class_code!r}, quot_ref={self.class_name!r})"


class t__Product(Base):
    prod_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prod_code: Mapped[str] = mapped_column(index=True)
    prod_desc: Mapped[str] = mapped_column(index=True)
    prod_frz_flag: Mapped[bool] = mapped_column()
    pol_trans_dflt: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Relation to Quote - up
    prod_class_sys_id: Mapped[int] = mapped_column(
        ForeignKey("t__uwclass.class_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    t__uwclass: Mapped["t__UwClass"] = relationship(back_populates="t__products")

    # Many-to-Many Relation to Section - down
    t__sections: Mapped[list["t__Section"]] = relationship(secondary="t__productsectionassociation",
                                                           back_populates="t__products")


class t__ProductSectionAssociation(Base):
    prod_sys_id: Mapped[int] = mapped_column(ForeignKey("t__product.prod_sys_id"), primary_key=True)
    sec_sys_id: Mapped[int] = mapped_column(ForeignKey("t__section.sec_sys_id"), primary_key=True)
    sec_trans_dflt: Mapped[str] = mapped_column(JSONB, nullable=True)


class t__Section(Base):
    sec_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sec_code: Mapped[str] = mapped_column(index=True)
    sec_desc: Mapped[str] = mapped_column(index=True)
    sec_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Product - up
    t__products: Mapped[list[t__Product]] = relationship(secondary="t__productsectionassociation",
                                                         back_populates="t__sections")

    # Many-to-Many Relation to Risk - down
    t__risks: Mapped[list["t__Risk"]] = relationship(secondary="t__sectionriskassociation",
                                                     back_populates="t__sections")


class t__SectionRiskAssociation(Base):
    sec_sys_id: Mapped[int] = mapped_column(ForeignKey("t__section.sec_sys_id"), primary_key=True)
    risk_sys_id: Mapped[int] = mapped_column(ForeignKey("t__risk.risk_sys_id"), primary_key=True)
    risk_trans_dflt: Mapped[str] = mapped_column(JSONB, nullable=True)


class t__Risk(Base):
    risk_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    risk_code: Mapped[str] = mapped_column(index=True)
    risk_desc: Mapped[str] = mapped_column(index=True)
    risk_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Section - up
    t__sections: Mapped[list[t__Section]] = relationship(secondary="t__sectionriskassociation",
                                                         back_populates="t__risks")

    # Many-to-Many Relation to Cover - down
    t__covers: Mapped[list["t__Cover"]] = relationship(secondary="t__riskcoverassociation", back_populates="t__risks")


class t__RiskCoverAssociation(Base):
    risk_sys_id: Mapped[int] = mapped_column(ForeignKey("t__risk.risk_sys_id"), primary_key=True)
    cvr_sys_id: Mapped[int] = mapped_column(ForeignKey("t__cover.cvr_sys_id"), primary_key=True)
    cvr_trans_dflt: Mapped[str] = mapped_column(JSONB, nullable=True)


class t__Cover(Base):
    cvr_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cvr_code: Mapped[str] = mapped_column(index=True)
    cvr_desc: Mapped[str] = mapped_column(index=True)
    cvr_frz_flag: Mapped[bool] = mapped_column()

    # Many-to-Many Relation to Section - up
    t__risks: Mapped[list[t__Risk]] = relationship(secondary="t__riskcoverassociation",
                                                         back_populates="t__covers")
