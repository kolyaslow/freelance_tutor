import logging
from typing import TYPE_CHECKING, Optional

from fastapi import Depends, HTTPException, Request, status
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.schemas_confirmation_keys import CreateConfirmationKeys
from api_v1.task_celery.send_email import generate_random_code, send_email
from core.config import settings
from core.db_helper import db_helper
from core.models import ConfirmationKeys
from core.models.user import User, get_user_db

from ..common import crud as common_crud
from . import crud as user_crud

if TYPE_CHECKING:
    from src.core.models import User


logger = logging.getLogger(__name__)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.jwt.SECRET_KEY_BY_JWT, lifetime_seconds=3600)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.jwt.SECRET_KEY_BY_UserManager
    verification_token_secret = settings.jwt.SECRET_KEY_BY_UserManager

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Отправка и фиксации кода подтвкердения на email"""

        logger.info(f"User {user.id} has registered.")
        email_confirmation_code = generate_random_code()
        message = f"Код для поддтверждения: {email_confirmation_code}"

        data = CreateConfirmationKeys(
            user_id=user.id, email_confirmation_code=email_confirmation_code
        )

        try:
            send_email.delay(user=user, message=message, subject="Подтверждение почты")
            logger.info(f"Successful sending of an email to a user: {user.email}")

            async with db_helper.session_factory() as session:
                await common_crud.create_db_item(
                    session=session,
                    model_db=ConfirmationKeys,
                    data=data,
                )
            logger.info(
                f"added an entry to the table ConfirmationKeys for user: {user.email}"
            )
        except Exception as e:
            logger.error("Error when sending an email: ", e)


async def verify_request(
    user_email,
    code,
    session: AsyncSession,
):
    """Првоерка почты пользователя и цстановка поля is_verified в значение true"""
    user = await user_crud.get_user_with_code(
        session=session,
        user_email=user_email,
    )

    if user.confirmation_keys.email_confirmation_code != code:
        logger.error(f"User {user_email}  entered an invalid code ")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный код подтверждения",
        )

    await user_crud.set_field_verified(
        session=session,
        user=user,
    )

    logger.info(f"User {user_email}  has been verified")
    return status.HTTP_200_OK


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
