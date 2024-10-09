import os
import random
import string
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any

import aiosmtplib
from faker import Faker
from fastapi import HTTPException
from jinja2 import FileSystemLoader, Environment
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas

sample = Faker()

# Set up Jinja2 environment
base_path = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(base_path, "email_templates")

# Configure Jinja2 template loader and environment
template_loader = FileSystemLoader(searchpath=templates_path)
template_env = Environment(loader=template_loader)


async def sample_user() -> schemas.UserCreateStrict:
    first_name = sample.first_name()
    last_name = sample.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    phone = sample.phone_number()
    nic = ''.join(random.choices(string.digits, k=8))  # 12867677
    pin = "A" + ''.join(random.choices(string.digits, k=10)) + "Z"  # "A1234567890D",
    password = "qwerty"

    # TODO Add functionality to check corporate

    user = schemas.UserCreateStrict(
        first_name=first_name,
        last_name=last_name,
        name=f"{first_name} {last_name}",
        email=email,
        username=email,
        phone=sample.phone_number(),
        nic=nic,
        pin=pin,
        password=password,
    )
    # user.premia_cust_payload=None
    return user


async def create_user(
        async_db: AsyncSession,
        user_in: schemas.UserCreate,
) -> models.User:
    user = await crud.user.create(async_db, obj_in=user_in)
    return user


async def get_agent(
        async_db: AsyncSession,
        search_criteria: dict[str, Any],
) -> models.User:
    agent_list = await crud.user.get_agent(async_db, search_criteria=search_criteria)
    return agent_list

async def get_user(
        async_db: AsyncSession,
        user_in: schemas.UserCreate,
) -> models.User:
    user_list = await crud.user.get_by_all(
        async_db, email=user_in.email, pin=user_in.pin, nic=user_in.nic
    )
    if not user_list == []:
        # if type(user_in) is schemas.UserCreateStrict:
        # Happens if doing Open user registration
        if isinstance(user_in, schemas.UserCreateStrict):
            raise HTTPException(
                status_code=400,
                detail="A user with these details already exists in the system",
            )
        # Happens while creating user via quotation. If multiple users are returned do not attach a user to the quotation i.e. user.id is 0
        if len(user_list) > 1:
            user = user_list[0]
            user.id = 0
            return user
            # raise HTTPException(
            #     status_code=400,
            #     detail="Mulitple users found. Contact your admin",
            # )
        # Happens while creating user via quotation. Since single user is returned, attach the user to the quote
        user_list_db = [
            models.User(**user) for user in user_list
        ]
        user = user_list_db[0]
    else:
        # Happens through both Open Registration and Quotation. User does not exist. Create the user (whether strict or via quotation)
        user = await create_user(async_db, user_in)

    return user


def generate_content(action_url, html_template, txt_template, user):
    context = {
        "activation_link": action_url,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "nic": user.nic,
        "pin": user.pin,
        "lic_no": user.lic_no,
    }
    # path_str = os.path.dirname(os.path.realpath(__file__))
    # templates = Jinja2Templates(directory=f"{path_str}/email_templates")
    # html_content = templates.TemplateResponse("new_user_activation.html", context)
    # html_content = render_template("new_user_activation.html", context)
    html_content = template_env.get_template(html_template).render({"context": context})

    # TODO: Implement textfiles"  # f"Hi {user.name}, {subject} by clicking this link: {action_url}. Or paste it in a browser and click go."
    plain_text_content = "Placeholder for plain text content"  # template_env.get_template(txt_template).render(context)
    return html_content, plain_text_content


async def generate_plain_text(action_url, template, user):
    context = {
        "activation_link": action_url,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "nic": user.nic,
        "pin": user.pin,
        "lic_no": user.lic_no,
    }
    # path_str = os.path.dirname(os.path.realpath(__file__))
    # templates = Jinja2Templates(directory=f"{path_str}/email_templates")
    # html_content = templates.TemplateResponse("new_user_activation.html", context)
    # html_content = render_template("new_user_activation.html", context)
    html_content = template_env.get_template(template).render({"context": context})
    return html_content


async def send_user_email(
        html_content: str,
        plain_text_content: str,
        from_email: str,
        to_emails: list[str],
        subject: str
) -> None:
    # html_content = await generate_html(action_url, template, user)
    # plain_text_content = f"Hi {user.name}, {subject} by clicking this link: {action_url}. Or paste it in a browser and click go."

    # Create the email message
    msg = MIMEMultipart("related")
    msg["Subject"] = subject  # "User Activation"
    msg["From"] = from_email
    msg["To"] = ", ".join(to_emails)

    # Create the alternative part to hold both plain text and HTML parts
    alternative_part = MIMEMultipart("alternative")
    alternative_part.attach(MIMEText(plain_text_content, "plain"))
    alternative_part.attach(MIMEText(html_content, "html"))

    # Attach the alternative part to the main message
    msg.attach(alternative_part)

    path_str = os.path.dirname(os.path.realpath(__file__))

    # Dictionary of images to attach
    images = {
        "background_2": f"{path_str}/email_templates/images/background_2.png",
        "header3": f"{path_str}/email_templates/images/header3.png",
        "logo": f"{path_str}/email_templates/images/logo.png",
        "facebook2x": f"{path_str}/email_templates/images/facebook2x.png",
        "instagram2x": f"{path_str}/email_templates/images/instagram2x.png",
        "twitter2x": f"{path_str}/email_templates/images/twitter2x.png",
        "Beefree-logo": f"{path_str}/email_templates/images/Beefree-logo.png",
    }

    # Attach images
    for cid, image_path in images.items():
        with open(image_path, "rb") as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header("Content-ID", f"<{cid}>")
            msg.attach(mime_image)

    # Send the email using aiosmtplib
    await aiosmtplib.send(
        msg,
        hostname="sandbox.smtp.mailtrap.io",
        port=2525,
        username="cced7a4e6b257e",
        password="2e8aecbb528b86",
        # start_tls=True
    )
