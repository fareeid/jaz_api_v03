from base64 import b64decode, b64encode
from typing import Any, AsyncGenerator, Generator

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad

from ..core.config import Settings, get_settings
from ..db.session import (
    async_session_local,
    oracledb_session_local,
    oracledb_session_local_sim,
)

settings: Settings = get_settings()
key = settings.DYN_MARINE_KEY.encode()  # type: ignore # get_random_bytes(16)


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
