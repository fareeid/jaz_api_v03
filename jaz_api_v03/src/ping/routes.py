import logging
import random
from typing import Any

from faker import Faker
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.config import Settings, get_settings
from ..core.dependencies import get_session
from . import crud_person, schemas

log = logging.getLogger("uvicorn")

router = APIRouter()

sample = Faker()


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
    return {"ping": "pong"}


@router.get("/env")
async def pong_env(settings: Settings = Depends(get_settings)) -> dict[Any, Any]:
    log.info("starting...")
    return {
        "ping_env": "pong_env",
        "POSTGRES_DB": settings.POSTGRES_DB,
        "environment": settings.SQLALCHEMY_DATABASE_URI,
    }


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
