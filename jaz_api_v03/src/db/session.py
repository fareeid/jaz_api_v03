from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from ..core.config import Settings, get_settings

settings: Settings = get_settings()


oracledb_engine = create_engine(settings.PREMIA_DATABASE_URI, pool_pre_ping=True)  # type: ignore  # noqa: E501
oracledb_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=oracledb_engine
)

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)  # type: ignore
async_session_local = async_sessionmaker(async_engine, expire_on_commit=False)
