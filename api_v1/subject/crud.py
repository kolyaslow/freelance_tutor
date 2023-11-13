from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi import status

from .schemas import CreateSubject
from core.models import Subject


async def get_subject(
        subject_name: str,
        session: AsyncSession,
) -> Subject | None:
    return await session.get(Subject, subject_name)


async def create_subject(
        session: AsyncSession,
        subject_in: CreateSubject,
) -> JSONResponse:
    subject = Subject(**subject_in.model_dump())
    session.add(subject)
    await session.commit()
    return JSONResponse(content={"message": "Entry created successfully"}, status_code=status.HTTP_201_CREATED)


async def delete_subject(
    session: AsyncSession,
    subject: Subject,
) -> None:
    await session.delete(subject)
    await session.commit()
