import os
from typing import AsyncGenerator, Any

import pytest
from sqlalchemy import create_engine, NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.testclient import TestClient

from ..src.auth import dependencies as auth_dependencies
from ..src.core.config import Settings
from ..src.core.dependencies import get_session
from ..src.db.base import Base
from ..src.main import create_application

non_async_db_url = f"postgresql://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_SERVER')}/{os.environ.get('POSTGRES_TEST_DB')}"
non_async_postgres_engine = create_engine(non_async_db_url, pool_pre_ping=True, )
Base.metadata.drop_all(non_async_postgres_engine)
Base.metadata.create_all(non_async_postgres_engine)

async_db_url = f"postgresql+asyncpg://{os.environ.get('POSTGRES_USER')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('POSTGRES_SERVER')}/{os.environ.get('POSTGRES_TEST_DB')}"
async_engine = create_async_engine(async_db_url, poolclass=NullPool, )  # type: ignore
async_test_session_local = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_session_override() -> AsyncGenerator[Any, Any]:
    async with async_test_session_local() as session:
        yield session


def fake_user_override():
    return "fake_user"


def get_settings_override():
    return Settings(TESTING="1", POSTGRES_DB=os.environ.get("POSTGRES_TEST_DB"), API_V1_STR="v1")


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    # app.dependency_overrides[get_settings] = get_settings_override
    app.dependency_overrides[get_session] = get_session_override
    app.dependency_overrides[auth_dependencies.get_current_user] = fake_user_override
    # print(non_async_postgres_engine)
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down
