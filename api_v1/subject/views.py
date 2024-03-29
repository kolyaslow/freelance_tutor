from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from core.models import Subject

from ..common.dependencies import user_rights
from . import crud
from .dependencies import get_subject
from .schemas import CreateSubject, SubjectRead

router = APIRouter()


@router.post(
    "/create_subject",
    dependencies=[Depends(user_rights.checking_superuser)],
    response_model=CreateSubject,
    status_code=status.HTTP_201_CREATED,
)
async def create_subject(
    subject_in: CreateSubject,
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Subject:
    try:
        subject = await crud.create_subject(session, subject_in)
        return subject
    except IntegrityError:  # обработка повторного создания объекта
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"An element with the same {subject_in.name} already exists",
        )


@router.delete(
    "/delete_subject/{subject_name}",
    dependencies=[Depends(user_rights.checking_superuser)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_subject(
    subject: Subject = Depends(get_subject),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    return await crud.delete_subject(session, subject)


@router.get(
    "/all_subjects",
    response_model=list[SubjectRead],
    dependencies=[Depends(user_rights.checking_current_user)],
)
async def get_all_subjects(
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> list["Subject"]:
    """Getting subjects that the tutor can choose from"""
    return await crud.get_all_subjects(session)
