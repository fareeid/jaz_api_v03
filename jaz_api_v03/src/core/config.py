import logging

# import secrets
from functools import lru_cache
from typing import Any, Union

from pydantic import FieldValidationInfo, PostgresDsn, field_validator
from pydantic_settings import BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file=".env")
    API_V1_STR: str = ""
    # SECRET_KEY: str = secrets.token_urlsafe(32) Use this to periodically generate secret at a python cli  # noqa: E501
    # SECRET_KEY: str = "0VgKaAreq7S6B1GZyiySv_QQ7NSGCHoNUONKoyZKU_A"

    SECRET_KEY: Union[str, None] = None

    @field_validator("SECRET_KEY")
    def create_test_env(cls, v: str, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return info.data["SECRET_KEY"]

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

    PREMIA_SERVER: Union[str, None] = None  # 10.158.2.24:1521
    PREMIA_USER: Union[str, None] = None  # P11_KE_LIVE
    PREMIA_PASSWORD: Union[str, None] = None  # p11_ke_live
    PREMIA_DB: Union[str, None] = None  # /?service_name=p11ke
    PREMIA_PORT: Union[int, None] = None  # 1521

    # "oracle+oracledb://P11_KE_LIVE:p11_ke_live@10.158.2.24:1521/?service_name=p11ke"
    # f"oracle+oracledb://{username}:{password}@{cp.host}:{cp.port}/?service_name={cp.service_name}"

    # PREMIA_DATABASE_URI: Union[
    #     str, None
    # ] = f"oracle+oracledb://{PREMIA_USER}:{PREMIA_PASSWORD}@{PREMIA_SERVER}:{PREMIA_PORT}/?service_name={PREMIA_DB}"

    PREMIA_DATABASE_URI: Union[str, None] = None

    @field_validator("PREMIA_DATABASE_URI")
    def assemble_premiadb_connection(cls, v: str, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        username = info.data["PREMIA_USER"]
        password = info.data["PREMIA_PASSWORD"]
        host = info.data["PREMIA_SERVER"]
        port = info.data["PREMIA_PORT"]
        db = info.data["PREMIA_DB"]
        conn_url = (
            f"oracle+oracledb://{username}:{password}@{host}:{port}/?service_name={db}"
        )
        return str(conn_url)

    RUNNING_IN_PRODUCTION: Union[str, None] = None

    @field_validator("RUNNING_IN_PRODUCTION")
    def prod_flag(cls, v: str, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return info.data["RUNNING_IN_PRODUCTION"]

    DYN_MARINE_KEY: Union[str, None] = None

    @field_validator("DYN_MARINE_KEY")
    def create_dyn_key_env(cls, v: str, info: FieldValidationInfo) -> Any:
        if isinstance(v, str):
            return v
        return info.data["DYN_MARINE_KEY"]

    USERS_OPEN_REGISTRATION: bool = True
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    P11_SERVER_SIM: str
    P11_USER_SIM: str
    P11_PASSWORD_SIM: str
    P11_DB_SIM: str

    PREMIA_DATABASE_URI_SIM: Union[str, None] = None

    @field_validator("PREMIA_DATABASE_URI_SIM")
    def assemble_premia_db_sim_connection(
        cls, v: str, info: FieldValidationInfo
    ) -> Any:
        if isinstance(v, str):
            return v
        # return info.data["POSTGRES_PASSWORD"]
        # postgresql+asyncpg://postgres:changethis@db:5432//app
        conn_url = PostgresDsn.build(
            scheme="postgresql",
            username=info.data["P11_USER_SIM"],
            password=info.data["P11_PASSWORD_SIM"],
            host=info.data["P11_SERVER_SIM"],
            path=f"{info.data['P11_DB_SIM'] or ''}",
        )
        print(conn_url)
        return str(conn_url)


@lru_cache()
def get_settings() -> Settings:
    log.info("Loading config settings from the .env...")
    return Settings()
