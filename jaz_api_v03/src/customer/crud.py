from typing import Any

from sqlalchemy import MetaData, Table, select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401

from ..db.session import oracledb_engine, postgres_engine

premia_metadata = MetaData()
web_dev_metadata = MetaData()


def get_customer(nic: str) -> list[Any]:
    with oracledb_engine.connect() as conn:
        pcom_customer = Table("pcom_customer", premia_metadata, autoload_with=conn)
        # pcom_customer.insert().values()
        stmt = select(pcom_customer).where(
            pcom_customer.c.cust_civil_id == "A009596174Z"
            or pcom_customer.c.cust_ref_no == "32079247"
            or pcom_customer.c.cust_email1 == "spokane.agency@gmail.com"
        )
        result = conn.execute(stmt)

    return list(result.scalars().all())


def get_cust_by_nic(nic: str) -> list[Any]:
    with oracledb_engine.connect() as conn:
        pcom_customer = Table("pcom_customer", premia_metadata, autoload_with=conn)
        # pcom_customer.insert().values()
        result = conn.execute(
            select(pcom_customer.c.cust_name).where(
                pcom_customer.c.cust_code == "152917x"
                or pcom_customer.c.cust_code == "152918"
            )
        )

    return list(result.scalars().all())


def get_cust_by_pin(pin: str) -> None:
    ...


def get_cust_by_email(email: str) -> None:
    ...


def get_proposal_table() -> Any:
    with postgres_engine.connect() as conn:
        proposal_tab = Table("proposal", web_dev_metadata, autoload_with=conn)

    # result = await async_db.execute(select(proposal).where(proposal.c.id == id))
    # return list(result.scalars().all())
    # return {"test_key": "test_value"}
    return proposal_tab


# async def get(async_db: AsyncSession, id: int) -> Any:
#     result = await async_db.execute()


# class CRUDCustomer:
#     async def get(self, oracle_db: Session, id: int) -> list[Any]:
#         result = await async_db.execute(select(self.model).where(self.model.id == id))
#         return list(result.scalars().all())
#         return list(result.scalars().all())
