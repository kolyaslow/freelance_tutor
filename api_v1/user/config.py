import os
from typing import TYPE_CHECKING, Optional
from dotenv import load_dotenv

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin

from core.models.user import User, get_user_db

if TYPE_CHECKING:
    from core.models import User

log = logging.getLogger(__name__)

load_dotenv()

# move to settings
# Setings Authentication backends
SECRET_KEY_BY_JWT = os.environ.get('SECRET_KEY_BY_JWT')
SECRET_KEY_BY_UserManager = os.environ.get('SECRET_KEY_BY_UserManager')

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_jwt_strategy() -> JWTStrategy:
    # lifetime_seconds -> settings
    return JWTStrategy(secret=SECRET_KEY_BY_JWT, lifetime_seconds=3600)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET_KEY_BY_UserManager
    verification_token_secret = SECRET_KEY_BY_UserManager

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # todo: logging
        print(f"User {user.id} has registered.")
        log.info("User %s has reg..", user.id)

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None,
    ):
        print(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None,
    ):
        print(f"Verification requested for user {user.id}. Verification token: {token}")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)