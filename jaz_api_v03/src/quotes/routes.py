import json
from base64 import b64decode, b64encode
from typing import Any

from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
from fastapi import APIRouter, Depends
from sqlalchemy import text  # Column, Integer, MetaData, String, Table, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from .models import Quote
from ..auth import dependencies as auth_dependencies
from ..auth import models as user_models
from ..auth import schemas as user_schemas
from ..auth import services as user_services
from ..core.dependencies import (  # , orcl_base
    aes_decrypt,
    aes_encrypt,
    get_oracle_session,
    get_oracle_session_sim,
    get_session,
)
from ..customer import crud as customers_crud

# from . import crud
from . import crud as quotes_crud
from . import (  # noqa: F401
    models,
    schemas,
    schemas_,
    vendors_api,  # noqa: F401
)
from . import services as quote_services
from .vendors_api import schemas as vendor_schemas

router = APIRouter()


@router.post("/quote", response_model=schemas.Quote)  # dict[str, Any]
async def quote(
    *,
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917")  # noqa: F841

    # Create User to attach to the quote. This is working. For now quotes will be
    # created without bona fide users.
    user_obj = user_schemas.UserCreate(
        first_name=payload_in.quot_assr_name,
        name=payload_in.quot_assr_name,
        email=payload_in.quot_assr_email,
        phone=payload_in.quot_assr_phone,
        nic=payload_in.quot_assr_nic,
        pin=payload_in.quot_assr_pin,
    )
    user = await user_services.get_user(async_db, user_obj)
    payload_in.quot_assr_id = user.id
    # noinspection PyShadowingNames
    quote: Quote = await quotes_crud.quote.create_v1(async_db, obj_in=payload_in)
    return quote
    # return {"test_key": "test_value"}


@router.post("/dyn_marine_payload", response_model=str)
async def dyn_marine_payload(
    *,
    current_user: user_models.User = Depends(auth_dependencies.get_current_user),
    async_db: AsyncSession = Depends(get_session),
    oracle_db: Session = Depends(get_oracle_session_sim),
    payload_in: vendor_schemas.QuoteMarineEncCreate,
) -> Any:
    # obj_in = {"pl_data": payload_in}
    payload = await quotes_crud.payload.create_v2(  # noqa: F841
        async_db, obj_in=payload_in
    )

    data = aes_decrypt(payload_in.MCINotification)
    data_dict = json.loads(data)

    payload_updated = await quotes_crud.payload.update(  # noqa: F841
        async_db, db_obj=payload, obj_in={"payload": data_dict}
    )

    data_schema = vendor_schemas.QuoteMarineCreate(**data_dict)

    # noinspection PyShadowingNames
    quote: Quote = await quote_services.create_quote(  # noqa: F841
        async_db, oracle_db, data_schema
    )

    resp = '{"status": "00", "reference":"' + data_dict["Reference"] + '"}'
    # resp_json = json.dumps(resp)

    return aes_encrypt(resp)
    pass


@router.post("/test_encrypt", response_model=str)
async def test_encrypt(payload_in: str) -> Any:
    # Encrypting...
    data = payload_in.encode()
    key = b"abcdefghijk23456"  # get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_ECB)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    # ct_bytes = cipher.encrypt(data)
    # iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    # ct = ct_bytes.decode("utf-8")
    # enc_result = json.dumps({"ciphertext": ct})
    # print(enc_result)
    return ct


@router.post("/test_decrypt", response_model=dict[str, Any])
async def test_decrypt(payload_in: str) -> Any:
    # Decrypting...
    key = b"abcdefghijk23456"  # get_random_bytes(16)
    # b64 = json.loads(payload_in)
    # iv = b64decode(b64['iv'])
    ct = b64decode(payload_in.encode())
    cipher = AES.new(key, AES.MODE_ECB)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    # pt = cipher.decrypt(ct)
    pt_str = "".join(c for c in pt.decode() if c.isprintable())
    # print(pt_str)

    # return {"The payload is": pt.decode().rstrip()}
    # return pt.decode().replace("\n", "")
    # return pt.decode().replace("\n", "").strip()
    return json.loads(pt_str)


@router.post("/quote_cust")  # dict[str, Any] , response_model=schemas.Quote
async def quote_cust(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    # customer = customers_crud.get_customer("152917x")  # noqa: F841
    # return customer
    policy = customers_crud.get_tables()
    return policy
    # return {"test_key": "test_value"}


@router.post("/test_reflection")  # dict[str, Any] , response_model=schemas.Quote
async def test_reflection(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    async_db: AsyncSession = Depends(get_session),
    payload_in: schemas.QuoteCreate,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    proposal_table = customers_crud.get_proposal_table()  # noqa: F841
    # Policy = orcl_base.classes.pgit_policy
    # quote = await quotes_crud.quote.create_v1(async_db, obj_in=payload_in)

    return proposal_table.columns._all_columns
    # return {"test_key": "test_value"}


@router.post("/test_ora_conn")  # dict[str, Any] , response_model=schemas.Quote
def test_oracle(
    *,
    oracle_db: Session = Depends(get_oracle_session),
    # payload_in: schemas_.PartnerTransBase,
    # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    result = oracle_db.execute(text("select * from jick_t where rownum<=6"))
    return result.scalars().all()
