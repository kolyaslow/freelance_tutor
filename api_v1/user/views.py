from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import UserCreate, UserRead, UserProfile
from core import db_helper
from .user_manager import get_user_manager
from .config import auth_backend
from . import crud
# from .dependencies import current_user

from core.models import User

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

@router.post('/add_subject', status_code=status.HTTP_201_CREATED)
async def add_subjects_by_user(
        subjects: list[str],
        session: AsyncSession = Depends(db_helper.session_dependency),
        user: User = Depends(fastapi_users.current_user()),
) -> None:
    try:
        await crud.add_subjects_by_user(
            session=session,
            user=user,
            subjects=subjects,
        )
    except IntegrityError: #обработка повторного создания объекта
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User have subject {subjects}"
        )


@router.get('/get_subject')
async def get_subjects_by_user(
        session: AsyncSession = Depends(db_helper.session_dependency),
        user: User = Depends(fastapi_users.current_user())
) -> list[str]:
    return await crud.get_subjects_by_user(
        session=session,
        user=user
    )

@router.get('/show_user_with_profile', response_model=UserProfile)
async def show_user_with_profile(
        session: AsyncSession = Depends(db_helper.session_dependency),
        user: User = Depends(fastapi_users.current_user())
) -> UserProfile | None:
    return await crud.show_user_with_profile(
        session=session,
        user=user
    )