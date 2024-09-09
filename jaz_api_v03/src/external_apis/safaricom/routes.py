import json
from typing import Any

import requests
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from requests.auth import HTTPBasicAuth
from sqlalchemy.ext.asyncio import AsyncSession

from .. import crud as external_apis_crud
from ...core.dependencies import get_session

router = APIRouter()


@router.post("/dyn_payload", response_model=dict[str, Any])
async def dyn_payload(
        *,
        async_db: AsyncSession = Depends(get_session),
        # oracle_db: Session = Depends(get_oracle_session_sim),
        payload_in: dict[str, Any],
) -> Any:
    data = {
        "external_party": "safaricom",
        "transaction_type": "CustomerPayBillOnline",
        "notification": "json",
        "payload": payload_in,
    }
    payload = await external_apis_crud.external_payload.create_v2(
        async_db, obj_in=data
    )
    return payload.__dict__['payload']


@router.post("/stk_push", response_model=dict[str, Any])  # dict[str, Any]
async def stk_push(
        *,
        async_db: AsyncSession = Depends(get_session),
        # oracle_db: Session = Depends(get_oracle_session_sim),
        payload_in: dict[str, Any],
) -> Any:
    oauth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate"
    username = "S1kv9CR1qrj233YLn5Jt81J2TNkpNvQpygG7WShCdgrN7aSG"
    password = "hJ0bgIGPBHxh6Xzc2U9i2iXdYADjVTXC3DNNzjyVFZIpIh1UMaw0hhlfMN0ILCS5"
    grant_type = "client_credentials"  # or any other value you want to use
    auth = HTTPBasicAuth(username, password)

    params = {"grant_type": grant_type}
    response = requests.get(oauth_url, auth=auth, params=params)

    access_token = response.json()["access_token"]

    # access_token = "m0hOUG6GbjA5lHn4QTvCvkRKmbv5"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    payload = {
        "BusinessShortCode": "174379",
        "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
        "Timestamp": "20160216165627",
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "1",
        "PartyA": "254722965810",
        "PartyB": "174379",
        "PhoneNumber": "254722965810",
        "CallBackURL": "https://jazk-api-app2.victoriousriver-e1958513.northeurope.azurecontainerapps.io/quotes/dyn_marine_payload",
        "AccountReference": "Test",
        "TransactionDesc": "Test"
    }
    payload_json = jsonable_encoder(payload)

    response = requests.post('https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest', headers=headers, json=payload_json)
    response_json = json.loads(response.text)
    formatted_response = jsonable_encoder(response_json)
    print(response.text.encode('utf8'))
    return response_json
