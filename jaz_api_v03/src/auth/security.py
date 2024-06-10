from datetime import datetime, timedelta
from typing import Any, Union

import bcrypt
from jose import jwt

# Depracated due to AttributeError: module 'bcrypt' has no attribute '__about__'
# passlib is not longer actively maintained
# https://github.com/pyca/bcrypt/issues/684
from passlib.context import CryptContext

from ..core.config import Settings, get_settings

settings: Settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
    subject: Union[str, Any], expires_delta: Union[timedelta, None] = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Depracated due to AttributeError: module 'bcrypt' has no attribute '__about__'
def verify_passwordx(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Depracated due to AttributeError: module 'bcrypt' has no attribute '__about__'
def get_password_hashx(password: str) -> str:
    return pwd_context.hash(password)


# Use this to avoid above error in docker
# Hash a password using bcrypt
def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode(encoding="utf-8")


# Use this to avoid above error in docker
# Check if the provided password matches the stored password (hashed)
def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode("utf-8")
    hashed_pass_byte_enc = hashed_password.encode("utf-8")
    return bcrypt.checkpw(
        password=password_byte_enc, hashed_password=hashed_pass_byte_enc
    )
