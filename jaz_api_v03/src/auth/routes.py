from datetime import timedelta
from enum import Enum
from typing import Any

# from faker import Faker
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request, Body, Path
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from . import crud, dependencies, models, schemas, security, services
from ..core.config import Settings, get_settings
from ..core.dependencies import get_session, get_non_async_oracle_session  # Real database
# from ..core.dependencies import get_session, \
#     get_oracle_session_sim as get_non_async_oracle_session  # simulation postgres_session
from ..premia import services as premia_services

# sample = Faker()

router = APIRouter()

settings: Settings = get_settings()


class Source(str, Enum):
    quote = "quote"
    user = "user"


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

@router.get("/sample_user", response_model=dict[str, Any])  # schemas.User
async def sample_user() -> Any:
    return await services.sample_user()


@router.post("/register_agent", response_model=dict[str, Any])  # list[schemas.User] schemas.User
async def register_agent(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        agent_in: schemas.UserRegisterAgent,
        background_tasks: BackgroundTasks,
        request: Request,
) -> Any:
    # user = await services.get_user(async_db, agent_in)
    search_criteria = {"cust_code": agent_in.cust_code, "email": agent_in.email, "phone": agent_in.phone}
    agent_list = await services.get_agent(async_db, search_criteria=search_criteria)

    if len(agent_list) == 0:
        premia_cust_search_criteria = {"cust_code": agent_in.cust_code, "cust_email1": agent_in.email,
                                       "cust_mobile_no": agent_in.phone}
        customer_model_list = premia_services.get_customer(non_async_oracle_db,
                                                           search_criteria=premia_cust_search_criteria)
        if len(customer_model_list) == 0:
            raise HTTPException(status_code=500,
                                detail="Your details do not match any of our records. Please contact the Agents Administrator")
        elif len(customer_model_list) == 1:
            agent_in.first_name = customer_model_list[0].cust_first_name
            agent_in.last_name = customer_model_list[0].cust_last_name
            agent_in.name = customer_model_list[0].cust_name
            agent_in.username = customer_model_list[0].cust_mobile_no  #customer_model_list[0].cust_email1
            agent_in.pin = customer_model_list[0].cust_civil_id
            agent_in.nic = customer_model_list[0].cust_ref_no
            agent_in.cust_cc_code = customer_model_list[0].cust_cc_code
            agent_in.cust_customer_type = customer_model_list[0].cust_customer_type
            # agent_in.lic_no = customer_model_list[0].cust_ref_no
            user = await services.create_user(async_db, agent_in)
        else:
            raise HTTPException(status_code=400,
                                detail="Multiple records found. Please contact the Agents Administrator")
    elif len(agent_list) == 1:
        agent = agent_list[0]
        raise HTTPException(status_code=400, detail="Agent already registered as portal user. Please log in")
    else:
        raise HTTPException(status_code=400, detail="Multiple records found. Please contact the Agents Administrator")

    activation_url = await services.generate_activation_url(request, user)
    # activation_token_expires = timedelta(minutes=settings.ACTIVATION_TOKEN_EXPIRE_MINUTES)
    # user_activation_token = security.create_token(user.username, expires_delta=activation_token_expires)
    # base_url = str(request.base_url).rstrip("/")
    # activation_url = f"{base_url}/auth/activate?token={user_activation_token}"

    await services.send_new_user_email(activation_url, background_tasks, user)

    # TODO Add functionality to approve agent & staff requests
    # TODO Create environment variable for send_from email

    # return f"{base_url}/activate?token={user_activation_token}"
    # print(activation_url)
    # return {"activation_url": json.dumps(activation_url), "username": user.username}
    # return user
    return {"message": "Portal user registered Please send activation email",
            "activation_url": activation_url,
            # "html_content": html_content,
            }


@router.post("/create_user/{source}", response_model=dict[str, Any])  # list[schemas.User] schemas.User
async def create_user(
        *,
        async_db: AsyncSession = Depends(get_session),
        non_async_oracle_db: Session = Depends(get_non_async_oracle_session),  # Real Premia
        # async_oracle_db: Session = Depends(get_async_oracle_session),
        # non_async_oracle_db: Session = Depends(get_oracle_session_sim),       # Simulation Premia
        user_in: schemas.UserCreateSelf,
        source: str = Path(..., description="Source should be quote or user"),
        background_tasks: BackgroundTasks,
        request: Request,
) -> Any:
    """
    Create new user without the need to be logged in.
    """
    if source not in Source.__members__.values():
        allowed_values = ", ".join([f.value for f in Source])
        raise HTTPException(
            status_code=400,
            detail=f"Invalid '{source}'. Please enter one of the following: quote."
            # detail = f"Invalid '{source}'. Please enter one of the following: {allowed_values}."
        )

    if settings.DEV_STATUS == "API_DEV":
        user_in = await sample_user()
    if settings.DEV_STATUS == "WEB_DEV":
        pass
    if settings.DEV_STATUS == "NO_DEV":
        pass
    if source == "user":
        if not settings.USERS_OPEN_REGISTRATION:
            raise HTTPException(
                status_code=403,
                detail="Open user registration is forbidden on this server",
            )
    # TODO: Seperate get and create user functions
    # Creates or returns an existing user
    new, user = await services.get_user(async_db, user_in)
    activation_url = ""
    message = "User already exists. Please log in"
    if new:
        activation_url = await services.generate_activation_url(request, user)
        await services.send_new_user_email(activation_url, background_tasks, user)
        message = "A new Portal user has been registered. Please send an activation email. You can also log this user in and buy policy"
    if source == "quote":
        customer_model = await sync_user_to_premia_cust(non_async_oracle_db, user)
        if customer_model and not user.cust_code:
            user = await crud.user.update(async_db, db_obj=user,
                                          obj_in={"cust_code": customer_model.cust_code, "is_active": True})

    return_dict = {"message": message,
                   "activation_url": activation_url,
                   "user": jsonable_encoder(user,
                                            exclude_unset=True,
                                            exclude_none=True,
                                            include={"name",
                                                     "email",
                                                     "phone",
                                                     "pin",
                                                     "lic_no",
                                                     "nic",
                                                     "dob",
                                                     "gender",
                                                     "user_flexi",})}

    return return_dict


async def sync_user_to_premia_cust(non_async_oracle_db, user):
    customer_model_list = premia_services.get_premia_customer(non_async_oracle_db, user)
    if len(customer_model_list) == 0:
        customer_model = premia_services.create_premia_customer(non_async_oracle_db, user)
    elif len(customer_model_list) == 1:
        customer_model = customer_model_list[0]
    else:
        raise HTTPException(status_code=400,
                            detail="Multiple records found. Please contact the Agents Administrator")
    return customer_model


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
        base_url = str(request.base_url).rstrip("/")
        recovery_url = f"{base_url}/auth/reset-password?token={password_reset_token}"
        html_content, plain_text_content = services.generate_content(action_url=None,
                                                                     html_template="password_recovery.html",
                                                                     txt_template="", user=user_list[0])
        background_tasks.add_task(services.send_user_email, html_content, recovery_url, password_reset_token,
                                  "password_recovery.html", "Reset Password")

        # return f"{base_url}/activate?token={password_reset_token}"
        # print(recovery_url)
        return {
            "message": f"Send the user a link to a form that posts this token and new password to {base_url}/auth/reset-password. {{token:'password_reset_token',new_password:'password'}}",
            "password_reset_token": password_reset_token, "username": user_list[0].username}
    else:
        raise HTTPException(status_code=401, detail="Invalid email or token")


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
        # if not user_list[0].is_active:
        #     # TODO: Resend account activation email or redirect to user registration
        #     return {"message": "Account is not activated.", "username": user_list[0].username,
        #             "is_active": user_list[0].is_active}
        hashed_password = security.get_password_hash(new_password)
        user = await crud.user.update(async_db, db_obj=user_list[0],
                                      obj_in={"password": hashed_password, "is_active": True})
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
        async_db,
        username=form_data.username,
        password=form_data.password
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
