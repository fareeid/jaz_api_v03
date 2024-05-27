# from typing import Any
# from sqlalchemy import MetaData
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.session import oracledb_engine_sim as oracledb_engine  # , postgres_engine

# web_dev_metadata = MetaData()
# web_dev_metadata.reflect(postgres_engine, only=["user"])
# PgBase = automap_base(metadata=web_dev_metadata)
# PgBase.prepare()
# User = PgBase.classes.user

# premia_metadata = MetaData()
# premia_metadata.reflect(oracledb_engine, only=["pgit_policy_apit"])
# OrclBase = automap_base(metadata=premia_metadata)
# OrclBase.prepare()
# # Policyx = premia_metadata.tables["pgit_policy_api"]
# Policy = OrclBase.classes.pgit_policy_apit

OrclBase = automap_base()


class Policy(OrclBase):  # type: ignore
    __tablename__ = "pgit_policy_apit"
    pol_sys_id: Mapped[int] = mapped_column(primary_key=True)
    pol_end_no_idx: Mapped[int] = mapped_column(primary_key=True)
    pol_end_sr_no: Mapped[int] = mapped_column(primary_key=True)

    # Releation to PolicySection - down
    policysection_collection: Mapped[list["PolicySection"]] = relationship(
        back_populates="policy",
        primaryjoin="and_(Policy.pol_sys_id==PolicySection.psec_pol_sys_id, Policy.pol_end_no_idx==PolicySection.psec_end_no_idx, Policy.pol_end_sr_no==PolicySection.psec_end_sr_no)",  # noqa: E501
        cascade="all, delete-orphan",
        lazy="subquery",
    )


class PolicySection(OrclBase):  # type: ignore
    __tablename__ = "pgit_pol_section_apit"
    psec_pol_sys_id: Mapped[int] = mapped_column(nullable=False)
    psec_end_no_idx: Mapped[int] = mapped_column(nullable=False)
    psec_end_sr_no: Mapped[int] = mapped_column(nullable=False)

    # Relation to Policy - up
    ForeignKeyConstraint(
        [psec_pol_sys_id, psec_end_no_idx, psec_end_sr_no],
        [
            Policy.pol_sys_id,
            Policy.pol_end_no_idx,
            Policy.pol_end_sr_no,
        ],
    )
    policy: Mapped["Policy"] = relationship(
        back_populates="policysection_collection",
        # primaryjoin="and_(Policy.pol_sys_id==PolicySection.psec_pol_sys_id, Policy.pol_end_no_idx==PolicySection.psec_end_no_idx, Policy.pol_end_sr_no==PolicySection.psec_end_sr_no)",  # noqa: E501
        # foreign_keys=[psec_pol_sys_id, psec_end_no_idx, psec_end_sr_no],
    )


OrclBase.prepare(
    autoload_with=oracledb_engine,
    reflection_options={"only": ["pgit_policy_apit", "pgit_pol_section_apit"]},
)  # noqa: E501
# OrclBase.prepare(
#     oracledb_engine, reflect=True, only=["pgit_policy_apit", "pgit_pol_section_apit"]
# )  # noqa: E501
# Policy = OrclBase.classes.pgit_policy_apit
# PolicySection = OrclBase.classes.pgit_pol_section_apit
pass
