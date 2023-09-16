from typing import Any, Union
from pydantic import FieldValidationInfo, PostgresDsn, field_validator
from pydantic_settings import BaseSettings
import logging
from functools import lru_cache

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env")

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Union[str, None] = None

    @field_validator("SQLALCHEMY_DATABASE_URI")
    def assemble_db_connection(cls, v: str, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        # return info.data["POSTGRES_PASSWORD"]
        # postgresql+asyncpg://postgres:changethis@db:5432//app
        conn_url = PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=info.data["POSTGRES_USER"],
            password=info.data["POSTGRES_PASSWORD"],
            host=info.data["POSTGRES_SERVER"],
            path=f"{info.data['POSTGRES_DB'] or ''}",
        )
        return str(conn_url)


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the .env...")
    return Settings()  # type: ignore
