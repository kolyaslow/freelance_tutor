from .user.config import auth_backend
from .user.schemas import UserRead, UserCreate
from .user.views import router as user_router, fastapi_users
from fastapi import APIRouter
from .subject.views import router as subject_router
from .profile.views import router as profile_router

router = APIRouter()

router.include_router(
    router=user_router,
    prefix='/user',
    tags=['User']
)

router.include_router(
    router=subject_router,
    prefix='/subject',
    tags=['Subject'],
)

router.include_router(
    router=profile_router,
    prefix='/profile',
    tags=['Profile'],
)

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