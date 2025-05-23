from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class Quote(Base):
    quot_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    quot_ref: Mapped[str] = mapped_column(index=True)
    quot_assr_id: Mapped[int] = mapped_column(nullable=True)
    quot_assr_name: Mapped[str] = mapped_column(nullable=True)
    quot_assr_nic: Mapped[str] = mapped_column(nullable=True)
    quot_assr_lic: Mapped[str] = mapped_column(nullable=True)
    quot_assr_pin: Mapped[str] = mapped_column(nullable=True)
    quot_assr_phone: Mapped[str] = mapped_column(nullable=True)
    quot_assr_email: Mapped[str] = mapped_column(nullable=True)
    quot_assr_gender: Mapped[str] = mapped_column(nullable=True)
    quot_assr_dob: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    quot_paymt_ref: Mapped[str] = mapped_column(nullable=True)
    quot_paymt_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    quot_paymt_amt: Mapped[float] = mapped_column(nullable=True)
    quot_assr_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Relation to Quote - up - Not neccesary at quote creation. But you can have it as null until client is ready to bind cover
    # quot_assr_id: Mapped[int] = mapped_column(
    #     ForeignKey("user.id"),
    #     nullable=True,
    # )

    # Releation to Proposal - down
    proposals: Mapped[list["Proposal"]] = relationship(
        back_populates="quote",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    def __repr__(self) -> str:
        return f"Quote(quot_sys_id={self.quot_sys_id!r}, quot_ref={self.quot_ref!r})"


class Proposal(Base):
    prop_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prop_sr_no: Mapped[int]
    prop_paymt_ref: Mapped[str] = mapped_column(nullable=True)
    prop_paymt_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    prop_paymt_amt: Mapped[float] = mapped_column(nullable=True)
    # prop_bank_cust_code: Mapped[str] = mapped_column(nullable=True)
    # prop_bank_cust_name: Mapped[str] = mapped_column(nullable=True)
    prop_hypothecation: Mapped[str] = mapped_column(JSONB, nullable=True)

    # input fields mapped to premia pgit_policy fields
    pol_quot_sys_id: Mapped[int] = mapped_column(nullable=True)
    pol_quot_no: Mapped[str] = mapped_column(nullable=True)
    pol_comp_code: Mapped[str] = mapped_column(nullable=False)
    pol_divn_code: Mapped[str] = mapped_column(nullable=False)
    pol_dept_code: Mapped[str] = mapped_column(nullable=True)
    pol_prod_code: Mapped[str] = mapped_column(nullable=False)
    pol_type: Mapped[str] = mapped_column(nullable=False)
    pol_cust_code: Mapped[str] = mapped_column(nullable=False)
    pol_assr_code: Mapped[str] = mapped_column(nullable=True)
    pol_hypothecation_yn: Mapped[str] = mapped_column(nullable=True)
    pol_fm_dt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pol_to_dt: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    pol_dflt_si_curr_code: Mapped[str] = mapped_column(nullable=False)
    pol_prem_curr_code: Mapped[str] = mapped_column(nullable=False)
    pol_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)
    pol_prd_sys_id: Mapped[int] = mapped_column(nullable=True)  # Link prop_sys_id to premia

    # output fields mapped from premia pgit_policy fields
    pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    pol_end_no_idx: Mapped[int] = mapped_column(nullable=True)
    pol_no: Mapped[str] = mapped_column(nullable=True)
    pol_cr_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    pol_appr_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    pol_sts: Mapped[str] = mapped_column(nullable=True)

    # Relation to Quote - up
    prop_quot_sys_id: Mapped[int] = mapped_column(
        ForeignKey("quote.quot_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    quote: Mapped["Quote"] = relationship(back_populates="proposals")

    # Relation to ProposalCharge - down
    proposalcharges: Mapped[list["ProposalCharge"]] = relationship(
        back_populates="proposal",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    # Relation to ProposalSection - down
    proposalsections: Mapped[list["ProposalSection"]] = relationship(
        back_populates="proposal",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    # Relation to ProposalPremium - down
    proposalpremiums: Mapped[list["ProposalPremium"]] = relationship(
        back_populates="proposal",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    def __repr__(self) -> str:
        return f"Proposal(prop_sys_id={self.prop_sys_id!r}, prop_quot_sys_id={self.prop_quot_sys_id!r})"  # noqa: E501


class ProposalPremium(Base):
    prem_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    prem_sr_no: Mapped[int] = mapped_column(nullable=True)
    prem_tot_amt: Mapped[float] = mapped_column(nullable=True)
    prem_curr_code: Mapped[str] = mapped_column(nullable=True)
    ad_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    ad_end_no_idx: Mapped[int] = mapped_column(nullable=True)
    ad_pol_no: Mapped[str] = mapped_column(nullable=True)
    ad_end_no: Mapped[str] = mapped_column(nullable=True)
    ad_doc_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    ad_tran_code_doc_no: Mapped[str] = mapped_column(nullable=True)
    ad_premium: Mapped[float] = mapped_column(nullable=True)
    ad_stamp_duty: Mapped[float] = mapped_column(nullable=True)
    ad_pcf: Mapped[float] = mapped_column(nullable=True)
    ad_itl: Mapped[float] = mapped_column(nullable=True)
    ad_comesa_fee: Mapped[float] = mapped_column(nullable=True)
    ad_road_rescue: Mapped[float] = mapped_column(nullable=True)
    ad_commission: Mapped[float] = mapped_column(nullable=True)
    ad_wht: Mapped[float] = mapped_column(nullable=True)

    # Relation to Proposal - up
    prem_prop_sys_id: Mapped[int] = mapped_column(
        ForeignKey("proposal.prop_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    proposal: Mapped["Proposal"] = relationship(back_populates="proposalpremiums")

    # Relation to ProposalInstallment - down
    proposalinstallments: Mapped[list["ProposalInstallment"]] = relationship(
        back_populates="proposalpremium",
        cascade="all, delete-orphan",
        lazy="subquery",
    )


class ProposalInstallment(Base):
    inst_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    inst_sr_no: Mapped[int] = mapped_column(nullable=True)
    inst_curr_code: Mapped[str] = mapped_column(nullable=True)
    inst_amt: Mapped[float] = mapped_column(nullable=True)
    inst_due_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    paymt_mode: Mapped[str] = mapped_column(nullable=True)
    paymt_ref: Mapped[str] = mapped_column(nullable=True)
    paymt_amt: Mapped[float] = mapped_column(nullable=True)
    paymt_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rcpt_no: Mapped[str] = mapped_column(nullable=True)
    rcpt_dt: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    rcpt_amt: Mapped[float] = mapped_column(nullable=True)

    # Relation to ProposalPremium - up
    inst_prem_sys_id: Mapped[int] = mapped_column(
        ForeignKey("proposalpremium.prem_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    proposalpremium: Mapped["ProposalPremium"] = relationship(back_populates="proposalinstallments")

    def __repr__(self) -> str:
        return f"ProposalInstallment(inst_sys_id={self.inst_sys_id!r}, inst_prop_sys_id={self.inst_prop_sys_id!r})"


class ProposalSection(Base):
    sec_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    sec_sr_no: Mapped[int]

    # Input fields mapped to premia pgit_pol_section fields
    psec_sec_code: Mapped[str] = mapped_column(nullable=False)
    psec_srno: Mapped[int] = mapped_column(nullable=True)
    psec_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Output fields mapped to premia pgit_pol_risk_addl_info fields
    psec_sys_id: Mapped[int] = mapped_column(nullable=True)
    psec_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    psec_end_no_idx: Mapped[int] = mapped_column(nullable=True)

    # Relation to Quote - up
    sec_prop_sys_id: Mapped[int] = mapped_column(
        ForeignKey("proposal.prop_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    proposal: Mapped["Proposal"] = relationship(back_populates="proposalsections")

    # Relation to ProposalRisk - down
    proposalrisks: Mapped[list["ProposalRisk"]] = relationship(
        back_populates="proposalsection",
        cascade="all, delete-orphan",
        lazy="subquery",
    )


class ProposalRisk(Base):
    risk_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    risk_sr_no: Mapped[int] = mapped_column(nullable=True)

    # Input fields mapped to premia pgit_pol_risk_addl_info fields
    prai_risk_sr_no: Mapped[int] = mapped_column(nullable=True)
    prai_data_18: Mapped[str] = mapped_column(nullable=True)  # 'Kenya'
    prai_code_03: Mapped[str] = mapped_column(nullable=True)  # '503'
    prai_desc_09: Mapped[str] = mapped_column(nullable=True)  # 'Residential'
    prai_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Output fields mapped to premia pgit_pol_risk_addl_info fields
    prai_sys_id: Mapped[int] = mapped_column(nullable=True)
    prai_risk_lvl_no: Mapped[int] = mapped_column(nullable=True)
    prai_risk_id: Mapped[str] = mapped_column(nullable=True)
    prai_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    prai_end_no_idx: Mapped[int] = mapped_column(nullable=True)

    # Relation to ProposalSection - up
    risk_sec_sys_id: Mapped[int] = mapped_column(
        ForeignKey(
            "proposalsection.sec_sys_id", ondelete="CASCADE", onupdate="CASCADE"
        ),
        nullable=False,
    )
    proposalsection: Mapped["ProposalSection"] = relationship(
        back_populates="proposalrisks"
    )

    # Relation to ProposalCover - down
    proposalcovers: Mapped[list["ProposalCover"]] = relationship(
        back_populates="proposalrisk",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    # Relation to ProposalSMI - down
    proposalsmis: Mapped[list["ProposalSMI"]] = relationship(
        back_populates="proposalrisk",
        cascade="all, delete-orphan",
        lazy="subquery",
    )

    # Relation to ProposalMotorCert - down
    proposalmotorcerts: Mapped[list["ProposalMotorCert"]] = relationship(
        back_populates="proposalrisk",
        cascade="all, delete-orphan",
        lazy="subquery",
    )


class ProposalMotorCert(Base):
    motor_cert_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    motor_cert_sr_no: Mapped[int] = mapped_column(nullable=True)

    # Input fields mapped to premia pgit_pol_risk_addl_info fields
    prai_risk_sr_no: Mapped[int] = mapped_column(nullable=True)
    prai_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Output fields mapped to premia pgit_pol_risk_addl_info fields
    prai_sys_id: Mapped[int] = mapped_column(nullable=True)
    prai_risk_lvl_no: Mapped[int] = mapped_column(nullable=True)
    prai_risk_id: Mapped[str] = mapped_column(nullable=True)
    prai_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    prai_end_no_idx: Mapped[int] = mapped_column(nullable=True)

    # Relation to ProposalRisk - up
    motor_cert_risk_sys_id: Mapped[int] = mapped_column(
        ForeignKey(
            "proposalrisk.risk_sys_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    proposalrisk: Mapped["ProposalRisk"] = relationship(back_populates="proposalmotorcerts")


class ProposalSMI(Base):
    smi_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    smi_sr_no: Mapped[int] = mapped_column(nullable=True)

    # Input fields mapped to premia pgit_pol_risk_smi fields
    prs_smi_code: Mapped[str] = mapped_column(nullable=False)
    prs_sr_no: Mapped[int] = mapped_column(nullable=True)
    prs_rate: Mapped[float] = mapped_column(nullable=True)
    prs_rate_per: Mapped[float] = mapped_column(nullable=True)
    prs_si_fc: Mapped[float] = mapped_column(nullable=True)
    prs_prem_fc: Mapped[float] = mapped_column(nullable=True)
    prs_smi_desc: Mapped[str] = mapped_column(nullable=True)
    prs_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Output fields mapped to premia pgit_pol_risk_smi fields
    prs_sys_id: Mapped[int] = mapped_column(nullable=True)
    prs_lvl1_sys_id: Mapped[int] = mapped_column(nullable=True)
    prs_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    prs_end_no_idx: Mapped[int] = mapped_column(nullable=True)
    prs_psec_sys_id: Mapped[int] = mapped_column(nullable=True)

    # Relation to ProposalRisk - up
    smi_risk_sys_id: Mapped[int] = mapped_column(
        ForeignKey(
            "proposalrisk.risk_sys_id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )
    proposalrisk: Mapped["ProposalRisk"] = relationship(back_populates="proposalsmis")


class ProposalCover(Base):
    cvr_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    cvr_sr_no: Mapped[int]

    # Input fields mapped to premia pgit_pol_risk_cover fields
    prc_code: Mapped[str] = mapped_column(nullable=False)
    prc_sr_no: Mapped[int] = mapped_column(nullable=True)
    prc_rate: Mapped[float] = mapped_column(nullable=True)
    prc_rate_per: Mapped[float] = mapped_column(nullable=True)
    prc_si_curr_code: Mapped[str] = mapped_column(nullable=False)
    prc_prem_curr_code: Mapped[str] = mapped_column(nullable=False)
    prc_si_fc: Mapped[float] = mapped_column(nullable=True)
    prc_prem_fc: Mapped[float] = mapped_column(nullable=True)
    prc_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Output fields mapped to premia pgit_policy_risk_cover fields
    prc_sys_id: Mapped[int] = mapped_column(nullable=True)
    prc_lvl1_sys_id: Mapped[int] = mapped_column(nullable=True)
    prc_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    prc_end_no_idx: Mapped[int] = mapped_column(nullable=True)

    # Relation to ProposalRisk - up
    cvr_risk_sys_id: Mapped[int] = mapped_column(
        ForeignKey("proposalrisk.risk_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    proposalrisk: Mapped["ProposalRisk"] = relationship(back_populates="proposalcovers")


class ProposalCharge(Base):
    chg_sys_id: Mapped[int] = mapped_column(primary_key=True, index=True)
    chg_sr_no: Mapped[int] = mapped_column(nullable=True)

    # Input fields mapped to premia pgit_pol_charge fields
    pchg_code: Mapped[str]
    pchg_sr_no: Mapped[int] = mapped_column(nullable=True)
    pchg_type: Mapped[str]
    pchg_perc: Mapped[float] = mapped_column(nullable=True)
    pchg_chg_fc: Mapped[float] = mapped_column(nullable=True)
    pchg_prem_curr_code: Mapped[str] = mapped_column(nullable=False)
    pchg_rate_per: Mapped[float] = mapped_column(nullable=True)
    pchg_flexi: Mapped[str] = mapped_column(JSONB, nullable=True)

    # Output fields mapped to premia pgit_pol_charge fields
    pchg_sys_id: Mapped[int] = mapped_column(nullable=True)
    pchg_pol_sys_id: Mapped[int] = mapped_column(nullable=True)
    pchg_end_no_idx: Mapped[int] = mapped_column(nullable=True)

    # Relation to Proposal - up
    chg_prop_sys_id: Mapped[int] = mapped_column(
        ForeignKey("proposal.prop_sys_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
    proposal: Mapped["Proposal"] = relationship(back_populates="proposalcharges")

# Proposal backup_fields
# # input fields mapped to premia pgit_policy fields

# pol_flex_01: Mapped[str] = mapped_column(nullable=True)
# pol_flex_02: Mapped[str] = mapped_column(nullable=True)
# pol_flex_09: Mapped[str] = mapped_column(nullable=True)
# pol_flex_10: Mapped[str] = mapped_column(nullable=True)
# pol_flex_13: Mapped[str] = mapped_column(nullable=True)
# pol_flex_14: Mapped[str] = mapped_column(nullable=True)
# pol_flex_16: Mapped[str] = mapped_column(nullable=True)
# pol_flex_17: Mapped[str] = mapped_column(nullable=True)
# pol_flex_18: Mapped[str] = mapped_column(nullable=True)
