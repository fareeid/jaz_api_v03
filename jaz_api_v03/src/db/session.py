from sqlalchemy import create_engine, String, collate, event
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from ..core.config import Settings, get_settings

settings: Settings = get_settings()

oracledb_engine = create_engine(settings.NON_ASYNC_PREMIA_DATABASE_URI,
                                pool_pre_ping=True)  # type: ignore  # noqa: E501
oracledb_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=oracledb_engine
)

# these two lines perform the "database reflection" to analyze tables and relationships
# OBase = automap_base()
# OBase.prepare(oracledb_engine, reflect=True)

# conn_str = "postgresql://postgres:changethis@db:5432/web_dev" ---------Works only on debug  # noqa: E501
# conn_str = "postgresql://postgres:changethis@db:5432/web_test"
# postgres_engine = create_engine(conn_str, pool_pre_ping=True)  # noqa: E501
postgres_engine = create_engine(settings.NON_ASYNC_SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)  # noqa: E501
postgres_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=postgres_engine
)

# A Postgres engine to simulate a lightweight Premia DB
# oracle_conn_str_sim = "postgresql://postgres:changethis@db:5432/premia" ---------Works only on debug  # noqa: E501
oracledb_engine_sim = create_engine(
    settings.PREMIA_DATABASE_URI_SIM, pool_pre_ping=True  # type: ignore
)  # noqa: E501
oracledb_session_local_sim = sessionmaker(
    autocommit=False, autoflush=False, bind=oracledb_engine_sim
)

# TODO: Check timezone issues on Azure
# TODO: ALTER DATABASE your_database_name SET timezone TO 'Asia/Nairobi';
# async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, connect_args={"server_settings": {"timezone": "US/Eastern"}})
async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)  # type: ignore
async_session_local = async_sessionmaker(async_engine, expire_on_commit=False)


# # Define the event listener for the session to apply collation
# async def apply_collation(evt, connection, target):
#     # Apply collation dynamically to all string columns
#     for attr in target.__table__.columns:
#         if isinstance(attr.type, String):
#             attr = collate(attr, "case_insensitive")  # Apply collation dynamically
#
#
# # Register the before_execute event listener
# event.listen(AsyncSession, "before_execute", apply_collation)
