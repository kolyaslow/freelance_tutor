from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from core.db_helper import db_helper
from ..user import current_user
from . import crud
from .schemas import CreateSubject
from core.models import Subject
from .dependencies import get_subject



router = APIRouter(tags=['Subject'])


@router.post('/create_subject', dependencies=[Depends(current_user.get_superuser())])
async def create_subject(
        subject_in: CreateSubject,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> JSONResponse:
    return await crud.create_subject(session, subject_in)


@router.delete('/delete_subject/{subject_name}', dependencies=[Depends(current_user.get_superuser())])
async def delete_subject(
        subject: Subject = Depends(get_subject),
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> None:
    return await crud.delete_subject(session, subject)