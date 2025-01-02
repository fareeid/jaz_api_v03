from base64 import b64decode, b64encode
from typing import Any, AsyncGenerator, Generator

import oracledb
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from sqlalchemy import text, String, collate

from ..core.config import Settings, get_settings
from ..db.session import (
    async_session_local,
    oracledb_session_local,
    oracledb_session_local_sim,
    postgres_session_local,
)

settings: Settings = get_settings()
key = settings.DYN_MARINE_KEY.encode()  # type: ignore # get_random_bytes(16)


# DB Dependency
async def get_session() -> AsyncGenerator[Any, Any]:
    async with async_session_local() as session:
        # await session.execute(text("SET timezone = 'Africa/Nairobi'"))
        # await session.execute(text("SET timezone = 'US/Eastern'"))
        yield session


def get_non_async_session() -> Generator:
    try:
        db = postgres_session_local()
        yield db
    finally:
        db.close()


# Dependency to get an async connection
async def get_async_oracle_session():
    # async with oracledb.connect_async("oracle+oracledb://p11_ke_live:p11_ke_live@10.157.2.57:1521/p11ke") as connection:
    async with oracledb.connect_async(user="p11_ke_live", password="p11_ke_live",
                                      dsn="10.157.2.57:1521/p11ke") as connection:
        async with connection.cursor() as cursor:
            yield cursor


def get_non_async_oracle_session() -> Generator:  # type: ignore
    try:
        db = oracledb_session_local()
        # Set the session-specific parameters for case-insensitivity
        db.execute(text("ALTER SESSION SET NLS_COMP=LINGUISTIC"))
        db.execute(text("ALTER SESSION SET NLS_SORT=BINARY_CI"))
        yield db
    finally:
        db.close()


def get_oracle_session_sim() -> Generator:  # type: ignore
    try:
        db = oracledb_session_local_sim()
        yield db
    finally:
        db.close()


def aes_encrypt(data_in: str) -> Any:
    data = data_in.encode()
    # key = b"abcdefghijk23456"  # get_random_bytes(16)
    # print("Encrypt:" + key.decode())
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    ct = b64encode(ct_bytes).decode("utf-8")
    return ct


def aes_decrypt(data_in: str) -> Any:
    ct = b64decode(data_in.encode())
    # print("Decrypt:" + key.decode())
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    pt_str = "".join(c for c in pt.decode() if c.isprintable())
    # pt = cipher.decrypt(ct)
    return pt_str


# Define your custom collation function (use your desired collation name)
def apply_case_insensitive_collation(column):
    """ Apply case-insensitive collation dynamically to string columns. """
    if isinstance(column.type, String):  # Check if it's a string type column
        return collate(column, 'case_insensitive')  # Apply the custom collation
    return column
