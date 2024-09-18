import logging
import random
import urllib.parse as urlparse
from datetime import datetime
from typing import Any, Union

import pytz
from faker import Faker
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud_person, schemas
from ..core.config import Settings, get_settings
from ..core.dependencies import get_session

log = logging.getLogger("uvicorn")

router = APIRouter()
sample = Faker()

MAX_PRICE = 100.0
MAX_PRICE_CHANGE = 0.02


def test_data() -> Any:
    person = schemas.PersonCreate(
        email=sample.email(),
        password=sample.password(),
        full_name=sample.name(),
    )
    item_count = random.randint(0, 4)
    # item = schemas.ItemCreate(title=sample.items())
    items = [
        schemas.ItemCreate(
            title="item " + str(n + 1) + " - " + sample.word(),
            description=sample.sentence(),
        )
        for n in range(item_count)
    ]
    person.items = items
    return person


@router.get("/")
async def pong() -> dict[Any, Any]:
    return {"ping": "pong",
            "TESTING": 0, }


@router.get("/dev_status")
async def dev_status(settings: Settings = Depends(get_settings)) -> dict[Any, Any]:
    log.info("starting...")
    return {
        "ping_dev": "pong_dev",
        "DEV_STATUS": settings.DEV_STATUS,
    }


@router.get("/env_test")
async def pong_env(settings: Settings = Depends(get_settings)) -> dict[Any, Any]:
    log.info("starting...")
    return {
        "ping_env": "pong_env",
        "POSTGRES_DB": settings.POSTGRES_DB,
        "environment": settings.SQLALCHEMY_DATABASE_URI,
    }


@router.get("/current_time")
async def read_current_time(db: AsyncSession = Depends(get_session)):
    utc_now = datetime.now(pytz.utc)
    local_now = utc_now.astimezone(pytz.timezone("Africa/Nairobi"))
    return {"utc_time": utc_now.isoformat(), "local_time": local_now.isoformat()}


@router.get("/test_error_loggin")
async def test_error_loggin():
    raise ValueError("This is an intentional error for testing error logging!")

@router.get("/stock_data")
async def stock_data(q: Union[str, None] = None, callback: Union[str, None] = None) -> Any:
    form = {}
    querystr = "q=" + q if q else ""
    callbackstr = "callback=" + callback if callback else ""
    query_callback = f"{querystr}&{callbackstr}"
    form = dict(urlparse.parse_qsl(query_callback))
    body = '['
    if 'q' in form:
        quotes = []

        for symbol in urlparse.unquote_plus(form['q']).split(' '):
            price = random.random() * MAX_PRICE
            change = price * MAX_PRICE_CHANGE * (random.random() * 2.0 - 1.0)
            stock_dict = {"symbol": symbol, "price": price, "change": change}
            # quotes.append(json.dumps(stock_dict))
            quotes.append(jsonable_encoder(stock_dict))
            # quotes.append('{"symbol":"%s","price":%f,"change":%f}'
            #               % (symbol, price, change))

        body += ','.join(str(quotes).replace("'", '"') for quotes in quotes)

    body += ']'

    if 'callback' in form:
        body = '%s(%s);' % (form['callback'], body)
    print(body)
    return Response(content=body, media_type="text/javascript")
    # return body


@router.get("/gwt_static/stockwatcher/stock_data_local", response_model=list[schemas.Stock])
async def stock_data_local(q: Union[str, None] = None) -> Any:
    form = {}
    querystr = "q=" + q if q else ""
    form = dict(urlparse.parse_qsl(querystr))
    body = '['
    if 'q' in form:
        quotes = []

        for symbol in urlparse.unquote_plus(form['q']).split(' '):
            price = random.random() * MAX_PRICE
            change = price * MAX_PRICE_CHANGE * (random.random() * 2.0 - 1.0)
            stock = schemas.Stock(symbol=symbol, price=price, change=change)
            quotes.append(stock)

    return quotes


@router.get("/sample_person", response_model=schemas.PersonCreate)  #
async def sample_person(person: schemas.Person = Depends(test_data)) -> Any:
    return person


@router.post("/create_person", response_model=schemas.Person)
async def create_person(
        *,
        async_db: AsyncSession = Depends(get_session),
        person_in: schemas.PersonCreate,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new person.
    """
    person = await crud_person.person.create(async_db, obj_in=person_in)
    return person


@router.get("/{person_id}", response_model=list[schemas.Person])
async def read_person_by_id(
        person_id: int,
        # current_user: models.User = Depends(deps.get_current_active_user),
        async_db: AsyncSession = Depends(get_session),
) -> Any:
    """
    Get a specific user by id.
    """
    # person = schemas.Person(id=999)
    person = await crud_person.person.get(async_db, person_id)
    # if user == current_user:
    #     return user
    # if not crud.user.is_superuser(current_user):
    #     raise HTTPException(
    #         status_code=400, detail="The user doesn't have enough privileges"
    #     )
    return person


@router.get("/", response_model=list[schemas.Person])
async def read_persons(
        async_db: AsyncSession = Depends(get_session),
        skip: int = 0,
        limit: int = 100,
        # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Retrieve persons.
    """
    persons = await crud_person.person.get_multi(async_db, skip=skip, limit=limit)
    return persons


@router.put(
    "/{user_id}", response_model=schemas.Person
)  # response_model=schemas.Person
async def update_user(
        *,
        async_db: AsyncSession = Depends(get_session),
        person_id: int,
        person_in: schemas.PersonUpdate,
        # current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    person_list = await crud_person.person.get(async_db, person_id)
    if person_list == []:
        raise HTTPException(
            status_code=404,
            detail="The person with this username does not exist in the system",
        )
    person = await crud_person.person.update(
        async_db, db_obj=person_list[0], obj_in=person_in
    )
    return person


@router.delete("/{person_id}", response_model=schemas.Person)
async def delete_person(
        *,
        async_db: AsyncSession = Depends(get_session),
        person_id: int,
        # current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Delete a person.
    """
    person_list = await crud_person.person.get(async_db, person_id)
    if person_list == []:
        raise HTTPException(status_code=404, detail="Person not found")
    person = await crud_person.person.remove(async_db=async_db, id=person_id)
    return person
