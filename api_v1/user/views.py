from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from .config import fastapi_users
from . import crud
from core.models import User, Subject
from api_v1.profile.schemas import ReadProfile
from api_v1.subject.dependencies import get_subject
from ..common.dependencies import user_rights
from ..subject.schemas import AllowedValuesByName


router = APIRouter()


@router.post('/add_subject', status_code=status.HTTP_201_CREATED)
async def add_subjects_by_user(
        subjects: list[AllowedValuesByName],
        session: AsyncSession = Depends(db_helper.session_dependency),
        user: User = Depends(user_rights.checking_tutor),
) -> None:
    """Добавление предмета в список, которые ведет репетитор """
    try:
        await crud.add_subjects_by_user(
            session=session,
            user_id=user.id,
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
        user: User = Depends(user_rights.checking_tutor)
) -> list[str]:
    """Получение репетитором всех предметов, которые он ведет"""
    return await crud.get_subjects_by_user(
        session=session,
        user=user
    )


@router.get(
    '/show_all_tutor_by_subject/{subject_name}',
    dependencies=[Depends(fastapi_users.current_user())],
    response_model=list[ReadProfile]
)
async def show_all_tutor_by_subject(
        subject: Subject = Depends(get_subject),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ReadProfile]:
    """Получение профилей репетиторов по определенному предмету"""
    return await crud.show_all_tutor_by_subject(
        session=session,
        subject_name=subject.name
    )

























