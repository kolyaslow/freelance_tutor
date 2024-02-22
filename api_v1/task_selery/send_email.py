import logging
import smtplib
from email.mime.text import MIMEText
from random import random

from fastapi import HTTPException, status

from api_v1.task_selery.config import email_data
from core.models import User

logger = logging.getLogger(__name__)

import random
import string


def generate_random_code(length=4):
    characters = string.ascii_letters + string.digits  # буквы и цифры
    password = "".join(random.choice(characters) for i in range(length))
    return password


def send_email(
    user: User,
    message: str,
    subject: str,
):
    sender = email_data.SENDER_EMAIL
    password = email_data.PASSWORD_EMAIL

    server = smtplib.SMTP(
        email_data.smtp_host,
        email_data.port,
    )
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(message)
        msg["Subject"] = subject
        server.sendmail(sender, user.email, msg.as_string())
        logger.info(
            f"Успешная отправка письма на подтверждение почты пользователя: {user.email}"
        )
        return status.HTTP_200_OK

    except smtplib.SMTPAuthenticationError:
        logger.error("Неверный логин или пароль")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZE, detail="Неверный логин или пароль"
        )
