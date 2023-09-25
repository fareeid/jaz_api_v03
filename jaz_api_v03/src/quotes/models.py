from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class Quote(Base):
    quot_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quot_num: Mapped[str] = mapped_column(index=True)
    quot_paymt_ref: Mapped[str] = mapped_column(nullable=True)
    quot_paymt_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    quot_assr_phone: Mapped[str] = mapped_column(nullable=True)
    quot_assr_email: Mapped[str] = mapped_column(nullable=True)

    proposals: Mapped[list["Proposal"]] = relationship(
        back_populates="quote", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Quote(quot_sys_id={self.quot_sys_id!r}, quot_num={self.quot_num!r})"


class Proposal:
    prop_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prop_sr_no: Mapped[int]
    prop_paymt_ref: Mapped[str] = mapped_column(nullable=True)
    prop_paymt_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    # input fields mapped to premia pgit_policy fields
    pol_quot_sys_id: Mapped[int] = mapped_column(nullable=True)
    pol_quot_no: Mapped[str] = mapped_column(nullable=True)
    pol_comp_code: Mapped[str] = mapped_column(nullable=False)
    pol_divn_code: Mapped[str] = mapped_column(nullable=False)
    pol_prod_code: Mapped[str] = mapped_column(nullable=False)
    pol_type: Mapped[str] = mapped_column(nullable=False)
    pol_cust_code: Mapped[str] = mapped_column(nullable=False)
    pol_assr_code: Mapped[str] = mapped_column(nullable=False)
    pol_fm_dt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pol_to_dt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pol_dflt_si_curr_code: Mapped[str] = mapped_column(nullable=False)
    pol_prem_curr_code: Mapped[str] = mapped_column(nullable=False)
    pol_flex_01: Mapped[str] = mapped_column(nullable=True)
    pol_flex_02: Mapped[str] = mapped_column(nullable=True)
    pol_flex_09: Mapped[str] = mapped_column(nullable=True)
    pol_flex_10: Mapped[str] = mapped_column(nullable=True)
    pol_flex_13: Mapped[str] = mapped_column(nullable=True)
    pol_flex_14: Mapped[str] = mapped_column(nullable=True)
    pol_flex_16: Mapped[str] = mapped_column(nullable=True)
    pol_flex_17: Mapped[str] = mapped_column(nullable=True)
    pol_flex_18: Mapped[str] = mapped_column(nullable=True)
    # output fields mapped from premia pgit_policy fields
    pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    pol_end_no_idx: Mapped[int] = mapped_column(nullable=True)
    pol_no: Mapped[str] = mapped_column(nullable=True)
    pol_cr_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    pol_appr_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    pol_sts: Mapped[str] = mapped_column(nullable=True)

    prop_quot_sys_id: Mapped[int] = mapped_column(
        ForeignKey("quote.quot_sys_id", ondelete="CASCADE", onupdate="CASCADE")
    )
    quote: Mapped["Quote"] = relationship(back_populates="proposals")

    def __repr__(self) -> str:
        return f"Proposal(prop_sys_id={self.prop_sys_id!r}, prop_quot_sys_id={self.prop_quot_sys_id!r})"  # noqa: E501
