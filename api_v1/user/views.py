from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from api_v1.user.schemas import UserRead, UserCreate
from .user_manager import get_user_manager
from core.models.user import User
from .config import auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
