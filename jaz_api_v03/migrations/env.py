import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata


from src.auth import models as auth_models  # noqa: E402, F401
from src.db.base import Base  # noqa: E402, F401
from src.ping import models as ping_models  # noqa: E402, F401
from src.quotes import models  # noqa: E402, F401
from src.quotes.vendors_api import models  # noqa: F401, E402, F811
# from src.masters.models import Product, Charge, ProductChargeAssociation # noqa: F401, E402, F811
from src.masters import models as masters_models  # noqa: E402, F401
from src.masters import models1 as masters_models1  # noqa: E402, F401
# from src.masters.models import Division, Department, UwClass    # noqa: E402, F401
# from src.masters.models import Product, Charge, Condition, Section, Cover    # noqa: E402, F401
# from src.masters.models import ProductChargeAssociation, ProductConditionAssociation, ProductSectionAssociation, SectionCoverAssociation    # noqa: E402, F401
from src.external_apis import models as external_apis_models  # noqa: E402, F401

# from jaz_api_v03.src.db import Base
target_metadata = Base.metadata


# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.
def get_url():  # type: ignore
    from src.core.config import Settings, get_settings   # noqa: E402, F401

    settings: Settings = get_settings()

    # user = settings.POSTGRES_USER
    # password = settings.POSTGRES_PASSWORD
    # server = settings.POSTGRES_SERVER
    # db = settings.POSTGRES_DB
    # return f"postgresql://{user}:{password}@{server}/{db}"
    return settings.SQLALCHEMY_DATABASE_URI


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = get_url()  # config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()  # type: ignore
    connectable = async_engine_from_config(
        configuration,  # type: ignore
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # connectable = async_engine_from_config(
    #     config.get_section(config.config_ini_section, {}),
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
