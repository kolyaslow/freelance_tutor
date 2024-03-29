from fastapi import status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Subject, User

from .schemas import CreateSubject


async def get_subject(
    subject_name: str,
    session: AsyncSession,
) -> Subject | None:
    return await session.get(Subject, subject_name)


async def create_subject(
    session: AsyncSession,
    subject_in: CreateSubject,
) -> Subject:
    subject = Subject(**subject_in.model_dump())
    session.add(subject)
    await session.commit()
    return subject


async def delete_subject(
    session: AsyncSession,
    subject: Subject,
) -> None:
    await session.delete(subject)
    await session.commit()


async def get_all_subjects(session: AsyncSession) -> list[Subject]:
    stmt = select(Subject)
    subject = await session.scalars(stmt).all()
    return list(subject)
