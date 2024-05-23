from typing import Any, AsyncGenerator, Generator

from ..db.session import async_session_local, oracledb_session_local


# DB Dependency
async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session_local() as session:
        # async with session.begin():
        yield session


def get_oracle_session() -> Generator:  # type: ignore
    try:
        db = oracledb_session_local()
        yield db
    finally:
        db.close()


# orcl_base = OrclBase
