from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from ..core.config import Settings, get_settings

# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker


settings: Settings = get_settings()


# engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)  # type: ignore  # noqa: E501
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI)  # type: ignore
async_session_local = async_sessionmaker(async_engine, expire_on_commit=False)
