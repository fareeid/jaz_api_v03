# from typing import Any
# from sqlalchemy import MetaData
from typing import Type, Dict, Any

from pydantic import BaseModel, create_model, ConfigDict
from sqlalchemy import ForeignKeyConstraint, inspect  # , inspect
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeMeta

from ..db.session import oracledb_engine_sim as oracledb_engine  # , simulation postgres_engine

# from ..db.session import oracledb_engine  # , Real engine

# from ..db.session import async_oracledb_engine  # , postgres_engine

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


class Customer(OrclBase):  # type: ignore
    __tablename__ = "pcom_customer"
    cust_code: Mapped[str] = mapped_column(primary_key=True)


class DocNumberRange(OrclBase):
    __tablename__ = "pgim_doc_number_range"
    dnr_sys_id: Mapped[int] = mapped_column(primary_key=True)
    dnr_curr_no: Mapped[int] = mapped_column()


class Policy(OrclBase):  # type: ignore
    __tablename__ = "pgit_policy"
    pol_sys_id: Mapped[int] = mapped_column(primary_key=True)
    pol_end_no_idx: Mapped[int] = mapped_column(primary_key=True)
    pol_end_sr_no: Mapped[int] = mapped_column(primary_key=True)

    # Relation to PolicySection - down
    policysection_collection: Mapped[list["PolicySection"]] = relationship(
        back_populates="policy",
        primaryjoin="and_(Policy.pol_sys_id==PolicySection.psec_pol_sys_id, Policy.pol_end_no_idx==PolicySection.psec_end_no_idx, Policy.pol_end_sr_no==PolicySection.psec_end_sr_no)",
        # noqa: E501
        cascade="all, delete-orphan",
        lazy="subquery",
    )


class PolicySection(OrclBase):  # type: ignore
    __tablename__ = "pgit_pol_section"
    psec_sys_id: Mapped[int] = mapped_column(primary_key=True)
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
    # autoload_with=async_oracledb_engine,
    reflection_options={
        "only": ["pcom_customer", "pgim_doc_number_range", "pgit_policy", "pgit_pol_section"]
    },
)  # noqa: E501


# Define the to_dict method in a mixin class
class ToDictMixin:
    def to_dict(self):
        return {column.key: getattr(self, column.key) for column in self.__table__.columns}


# Extend the reflected Base to include the mixin
# class ExtendedBase(OrclBase, ToDictMixin):
#     __abstract__ = True


Customer.to_dict = ToDictMixin.to_dict


# mapper = inspect(Policy)
# mapper_section = inspect(PolicySection)


def create_pydantic_model(name: str, sqlalchemy_model: Type[DeclarativeMeta]) -> Type[BaseModel]:
    mapper = inspect(sqlalchemy_model)
    if mapper is None:
        raise ValueError(f"Could not inspect model {sqlalchemy_model}")

    fields: Dict[str, Any] = {}  # Initializes an empty dictionary to store the fields of the Pydantic model.
    for column in mapper.columns:
        python_type = column.type.python_type if hasattr(column.type, 'python_type') else str
        fields[column.key] = (python_type, None)

    return create_model(name, **fields)


# Create Pydantic models dynamically
PolicyBase = create_pydantic_model("PolicyBase", Policy)
PolicySectionBase = create_pydantic_model("PolicySectionBase", PolicySection)
CustomerBase = create_pydantic_model("CustomerBase", Customer)
CustomerBase.model_config = ConfigDict(from_attributes=True)


# print(type(PolicyBase) is BaseModel)

# Verification step
def verify_pydantic_model(pydantic_model: Type[BaseModel]) -> None:
    instance = pydantic_model()
    print(f"Model: {pydantic_model.__name__}")
    print(f"Fields: {list(instance.model_fields.keys())}")
    print(f"Is instance {type(instance).__name__} a Pydantic Basemodel? {isinstance(instance, BaseModel)}")


# Verify the created Pydantic models
verify_pydantic_model(PolicyBase)
verify_pydantic_model(PolicySectionBase)

# OrclBase.prepare(
#     oracledb_engine, reflect=True, only=["pgit_policy_apit", "pgit_pol_section_apit"]
# )  # noqa: E501
# Policy = OrclBase.classes.pgit_policy_apit
# PolicySection = OrclBase.classes.pgit_pol_section_apit
# pass
# x = type(Customer.cust_addr_01)
# pass
# mapper = inspect(Policy)
# # print(mapper.columns._all_columns)
# for value in list(mapper.attrs):
#     print(value.columns[0])
#     print(type(value))
# pass
# print(mapper.attrs)
# print(list(mapper.attrs))
# # Iterate over all columns in the pgit_policy_apit table
# for column in mapper.columns:
#     print(f"column: {column.key} - Type: {column.type}")
