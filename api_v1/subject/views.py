from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse


from core.db_helper import db_helper
from ..user import current_user
from . import crud
from .schemas import CreateSubject, SubjectRead
from core.models import Subject, User
from .dependencies import get_subject
from sqlalchemy.exc import IntegrityError


router = APIRouter(tags=['Subject'])

#create subject
@router.post('/create_subject', dependencies=[Depends(current_user.get_superuser())], response_model=None)
async def create_subject(
        subject_in: CreateSubject,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> JSONResponse | HTTPException:
    try:
        return await crud.create_subject(session, subject_in)
    except IntegrityError: #обработка повторного создания объекта
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"An element with the same {subject_in.name} already exists"
        )

#delete subject
@router.delete(
    '/delete_subject/{subject_name}',
    dependencies=[Depends(current_user.get_superuser())],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_subject(
        subject: Subject = Depends(get_subject),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    return await crud.delete_subject(session, subject)

#get all subjects
@router.get(
    '/all_subjects',
    response_model=list[SubjectRead],
    dependencies=[Depends(current_user.get_current_user())]
)
async def get_all_subjects(session: AsyncSession = Depends(db_helper.session_dependency)) -> list['Subject']:
    return await crud.get_all_subjects(session)

@router.get('/get_users/{subject_name}', dependencies=[Depends(current_user.get_current_user())])
async def get_users_by_subject(
        subject: Subject = Depends(get_subject),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> list[int]:
    """
    Getting all users for a specific subject
    """
    return await crud.get_users_by_subject(
        session=session,
        subject_name=subject.name
    )

