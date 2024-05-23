from typing import Any

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401
from sqlalchemy.ext.automap import automap_base

from ..db.session import oracledb_engine

premia_metadata = MetaData()
web_dev_metadata = MetaData()

premia_metadata.reflect(oracledb_engine, only=["pgit_policy_api"])
OrclBase = automap_base(metadata=premia_metadata)
OrclBase.prepare()

Policy = OrclBase.classes.pgit_policy


def get_tables() -> Any:
    premia_metadata.reflect(oracledb_engine, only=["pgit_policy"])
    OrclBase = automap_base(metadata=premia_metadata)
    OrclBase.prepare()
    Policy = OrclBase.classes.pgit_policy
    return Policy
