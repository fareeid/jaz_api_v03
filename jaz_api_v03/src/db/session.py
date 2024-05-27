from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker

from ..core.config import Settings, get_settings

settings: Settings = get_settings()


oracledb_engine = create_engine(settings.PREMIA_DATABASE_URI, pool_pre_ping=True)  # type: ignore  # noqa: E501
oracledb_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=oracledb_engine
)

# these two lines perform the "database reflection" to analyze tables and relationships
# OBase = automap_base()
# OBase.prepare(oracledb_engine, reflect=True)

# conn_str = "postgresql://postgres:changethis@db:5432/web_dev"
conn_str = "postgresql://postgres:changethis@localhost:5432/web_dev"
postgres_engine = create_engine(conn_str, pool_pre_ping=True)  # noqa: E501
postgres_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=postgres_engine
)


# conn_str = "postgresql://postgres:changethis@db:5432/web_dev"
oracle_conn_str_sim = "postgresql://postgres:changethis@localhost:5432/premia"
oracledb_engine_sim = create_engine(
    oracle_conn_str_sim, pool_pre_ping=True
)  # noqa: E501
oracledb_session_local_sim = sessionmaker(
    autocommit=False, autoflush=False, bind=oracledb_engine_sim
)

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)  # type: ignore
async_session_local = async_sessionmaker(async_engine, expire_on_commit=False)
