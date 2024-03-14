import logging
import smtplib
from email.mime.text import MIMEText
from random import random

from fastapi import HTTPException, status

from api_v1.task_celery.config import settings
from core.models import User

from .config import celery

logger = logging.getLogger(__name__)

import random
import string


def generate_random_code(length=4):
    characters = string.ascii_letters + string.digits  # буквы и цифры
    password = "".join(random.choice(characters) for i in range(length))
    return password


@celery.task
def send_email(
    user: User,
    message: str,
    subject: str,
):
    sender = settings.email.SENDER_EMAIL
    password = settings.email.PASSWORD_EMAIL

    server = smtplib.SMTP(
        settings.email.smtp_host,
        settings.email.port,
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
