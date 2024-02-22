from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.common.dependencies import user_rights
from api_v1.profile.schemas import ReadProfile
from api_v1.subject.dependencies import get_subject
from core import db_helper
from core.models import Subject, User

from ..subject.schemas import AllowedValuesByName
from . import crud
from .config import verify_request
from .fastapi_user import fastapi_users

router = APIRouter()


@router.post("/add_subject", status_code=status.HTTP_201_CREATED)
async def add_subjects_by_user(
    subjects: list[AllowedValuesByName],
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(user_rights.checking_tutor),
) -> None:
    """Добавление предмета в список, которые ведет репетитор"""
    try:
        await crud.add_subjects_by_user(
            session=session,
            user_id=user.id,
            subjects=subjects,
        )
    except IntegrityError:  # обработка повторного создания объекта
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"User have subject {subjects}",
        )


@router.get("/get_subjects_by_user")
async def get_subjects_by_user(
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(user_rights.checking_tutor),
) -> list[str]:
    """Получение репетитором всех предметов, которые он ведет"""
    return await crud.get_subjects_by_user(session=session, user=user)


@router.get(
    "/show_all_tutor_by_subject/{subject_name}",
    dependencies=[Depends(fastapi_users.current_user())],
    response_model=list[ReadProfile],
)
async def show_all_tutor_by_subject(
    subject: Subject = Depends(get_subject),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[ReadProfile]:
    """Получение профилей репетиторов по определенному предмету"""
    return await crud.show_all_tutor_by_subject(
        session=session, subject_name=subject.name
    )


@router.delete("/delete_tutor_subjects")
async def delete_tutor_subjects(
    subjects: list[AllowedValuesByName],
    user: User = Depends(user_rights.checking_tutor),
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Удаляет предметы,, которые ведет репетитор"""
    await crud.delete_tutor_subjects(
        session=session,
        user_id=user.id,
        subjects_in=subjects,
    )


@router.post("/verify_user", status_code=status.HTTP_200_OK)
async def verify_user(
    user_email: EmailStr,
    code: str,
    session: AsyncSession = Depends(db_helper.session_dependency),
):
    """Проверяет код отпрравленный на опчту"""
    await verify_request(
        user_email=user_email,
        code=code,
        session=session,
    )
