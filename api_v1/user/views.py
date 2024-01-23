from fastapi import APIRouter, Depends, status, HTTPException
from fastapi_users import FastAPIUsers
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from .user_manager import get_user_manager
from .config import auth_backend
from . import crud
from core.models import User
from api_v1.profile.schemas import ReadProfile


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


router = APIRouter()


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


@router.get(
    '/show_all_tutor_by_subject',
    dependencies=[Depends(db_helper.session_dependency)],
    response_model=list[ReadProfile]
)
async def show_all_tutor_by_subject(
        subject_name: str,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ReadProfile]:
    """Получение профилей репетиторов по определенному предмету"""
    return await crud.show_all_tutor_by_subject(
        session=session,
        subject_name=subject_name
    )

























