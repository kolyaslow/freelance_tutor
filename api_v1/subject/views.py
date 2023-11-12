from starlette.responses import JSONResponse

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from ..user import fastapi_users
from . import crud
from .schemas import CreateSubject



router = APIRouter(tags=['Subject'])

@router.post('/create_subject', dependencies=[Depends(fastapi_users.current_user(optional=True, active=True,  superuser=True))])
async def create_subject(
        subject_in: CreateSubject,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> JSONResponse:
    return await crud.create_subject(session, subject_in)


@router.delete('/delete_subject', dependencies=[Depends(fastapi_users.current_user(optional=True, active=True,  superuser=True))])
async def delete_subject(
        subject_name: CreateSubject,
        session: AsyncSession = Depends(db_helper.session_dependency),
) -> JSONResponse:
    return await crud.delete_subject(session, subject_name)