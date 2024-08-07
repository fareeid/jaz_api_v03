import json
from datetime import timedelta, datetime
from typing import Any

# from faker import Faker
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import crud, dependencies, models, schemas, security, services
from ..core.config import Settings, get_settings
# from ..core.dependencies import get_session, get_non_async_oracle_session                              # Real database
from ..core.dependencies import get_session, \
    get_oracle_session_sim as get_non_async_oracle_session  # simulation postgres_session
from ..premia import services as premia_services

# sample = Faker()

router = APIRouter()

settings: Settings = get_settings()


# def sample_user() -> schemas.UserCreate:
#     user = schemas.UserCreate(
#         first_name=sample.first_name(),
#         last_name=sample.last_name(),
#         email=sample.email(),
#         username=sample.user_name(),
#         phone=sample.phone_number(),
#         password="qwerty12345",
#     )
#     return user

@router.get("/sample_user", response_model=schemas.User)  #
async def sample_user() -> Any:
    return await services.sample_user()


@router.post("/open", response_model=dict[str, Any])  # list[schemas.User] schemas.User
async def create_user_open(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),   # Real Premia
        # async_oracle_db: Session = Depends(get_async_oracle_session),
        # non_async_oracle_db: Session = Depends(get_oracle_session_sim),       # Simulation Premia
        user_in: schemas.UserCreateStrict,
        background_tasks: BackgroundTasks,
        request: Request,
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    if settings.DEV_STATUS == "API_DEV":
        user_in = await services.sample_user()

    if settings.DEV_STATUS == "WEB_DEV":
        pass

    if settings.DEV_STATUS == "NO_DEV":
        pass

    if not settings.USERS_OPEN_REGISTRATION:
        raise HTTPException(
            status_code=403,
            detail="Open user registration is forbidden on this server",
        )
    # Creates or returns an existing user
    user = await services.get_user(async_db, user_in)
    user = await crud.user.update(async_db, db_obj=user, obj_in={"created_by": user.id, "created_at": datetime.now()})

    activation_token_expires = timedelta(minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES)
    user_activation_token = security.create_token(user.username, expires_delta=activation_token_expires)
    base_url = str(request.base_url).rstrip("/")
    activation_url = f"{base_url}/auth/activate?token={user_activation_token}"

    # TODO: Create a txt file for new user registration
    html_content, plain_text_content = services.generate_content(action_url=activation_url,
                                                                 html_template="new_user_activation.html",
                                                                 txt_template="", user=user)

    background_tasks.add_task(services.send_user_email,
                              html_content, plain_text_content, settings.EMAILS_FROM_EMAIL,
                              [user.email], "Activate Account")

    # TODO Add functionality to approve agent & staff requests
    # TODO Create environment variable for send_from email

    search_criteria = {"cust_email1": user.email, "cust_civil_id": user.pin, "cust_ref_no": user.nic}
    # search_criteria = {"cust_email1": "sales@maishapoa.co.ke", "cust_civil_id": "P052205822V",
    #                    "cust_ref_no": "21960760"}

    # TODO: Convert from Premia simulation DB to real Premia DB. This works well
    customer_model_list = premia_services.get_customer(non_async_oracle_db, search_criteria=search_criteria)
    # customer_model_list = premia_services.get_customer(oracle_db, search_criteria=search_criteria)

    if len(customer_model_list) == 0:
        # TODO: Create a txt file for new premia customer
        html_content, plain_text_content = services.generate_content(action_url=None,
                                                                     html_template="new_premia_customer.html",
                                                                     txt_template="", user=user)

        background_tasks.add_task(services.send_user_email, html_content, plain_text_content,
                                  settings.EMAILS_FROM_EMAIL, ["nancy.nyanchogo@allianz.com"],
                                  "PREMIA Customer Required")
        # TODO: Create Customer code in Premia
        cust_code = premia_services.get_cust_code(non_async_oracle_db, cust_in=user)
        premia_cust_payload = user.premia_cust_payload
        premia_cust_payload["cust_code"] = cust_code
        premia_cust_payload["cust_cr_uid"] = "PORTAL-REG"
        premia_cust_payload["cust_cr_dt"] = user.created_at
        user = await crud.user.update(async_db, db_obj=user, obj_in={"cust_code": cust_code, "premia_cust_payload": premia_cust_payload})
        customer_model = premia_services.create_customer(non_async_oracle_db, premia_cust_payload=premia_cust_payload)
    # TODO: This path not tested yet
    elif len(customer_model_list) >= 2:
        # TODO: Create a txt file for duplicate premia customer
        html_content, plain_text_content = services.generate_content(action_url=None,
                                                                     html_template="duplicate_premia_customer.html",
                                                                     txt_template="", user=user)

        background_tasks.add_task(services.send_user_email, html_content, plain_text_content,
                                  settings.EMAILS_FROM_EMAIL, ["nancy.nyanchogo@allianz.com"],
                                  "PREMIA Customer Duplicated")


    elif len(customer_model_list) == 1:
        user = await crud.user.update(async_db, db_obj=user, obj_in={"cust_code": customer_model_list[0].cust_code,
                                                                     "cust_cc_code": customer_model_list[
                                                                         0].cust_cc_code, })

    # await services.send_new_user_activation_email(user, base_url, user_activation_token, "new_user_activation.html")

    # return f"{base_url}/activate?token={user_activation_token}"
    # print(activation_url)
    # return {"activation_url": json.dumps(activation_url), "username": user.username}
    # return user
    return {"message": "User created and activation email sent",
            "activation_url": activation_url,
            # "html_content": html_content,
            }


@router.get("/activate", response_model=dict[str, Any])  #schemas.User
async def user_activate(
        *,
        async_db: AsyncSession = Depends(get_session),
        token: str,
) -> Any:
    decoded_user_activation_token = security.verify_token(token)
    user_list = await crud.user.get_by_username(async_db, decoded_user_activation_token)
    if user_list:
        if user_list[0].is_active:
            return {"message": "Account is already activated.", "username": user_list[0].username,
                    "is_active": user_list[0].is_active}
        user = await crud.user.update(async_db, db_obj=user_list[0], obj_in={"is_active": True})
        return {"message": "Account is successfully activated.", "username": user_list[0].username,
                "is_active": user_list[0].is_active}
    else:
        raise HTTPException(status_code=401, detail="Invalid username or token")


@router.post("/password-recovery/{email}", response_model=dict[str, Any])
async def password_recovery(
        *,
        async_db: AsyncSession = Depends(get_session),
        email: str,
        background_tasks: BackgroundTasks,
        request: Request,
) -> Any:
    user_list = await crud.user.get_by_email(async_db, email)
    if user_list:
        activation_token_expires = timedelta(minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES)
        password_reset_token = security.create_token(email, expires_delta=activation_token_expires)
        base_url = str(request.url)
        recovery_url = f"{base_url}/auth/reset-password?token={password_reset_token}"
        background_tasks.add_task(services.send_user_email, user_list[0], recovery_url, password_reset_token,
                                  "password_recovery.html", "Reset Password")

        # return f"{base_url}/activate?token={password_reset_token}"
        print(recovery_url)
        return {"recovery_url": json.dumps(recovery_url), "username": user_list[0].username}
        # return user
        # return {"message": "User created and activation email sent"}


@router.post("/reset-password", response_model=dict[str, Any])  # schemas.User
async def reset_password(
        *,
        async_db: AsyncSession = Depends(get_session),
        token: str = Body(...),
        new_password: str = Body(...),
) -> Any:
    email = security.verify_token(token)
    user_list = await crud.user.get_by_email(async_db, email)
    if user_list:
        if not user_list[0].is_active:
            # TODO: Resend account activation email or redirect to user registration
            return {"message": "Account is not activated.", "username": user_list[0].username,
                    "is_active": user_list[0].is_active}
        hashed_password = security.get_password_hash(new_password)
        user = await crud.user.update(async_db, db_obj=user_list[0], obj_in={"password": hashed_password})
        return {"message": "Password is successfully reset.", "username": user_list[0].username,
                "is_active": user_list[0].is_active}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or token")


@router.post("/login/access-token", response_model=schemas.Token)
async def login_access_token(
        async_db: AsyncSession = Depends(get_session),
        form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await crud.user.authenticate(
        async_db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", response_model=schemas.User)
def test_token(
        current_user: models.User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Test access token
    """
    return current_user
