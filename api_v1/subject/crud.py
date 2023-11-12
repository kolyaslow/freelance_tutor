from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from .schemas import CreateSubject
from core.models import Subject

async def create_subject(
        session: AsyncSession,
        subject_in: CreateSubject,
) -> JSONResponse:
    subject = Subject(**subject_in.model_dump())
    session.add(subject)
    await session.commit()
    return JSONResponse(content={"message": "Entry created successfully"}, status_code=201)


async def delete_subject(
    session: AsyncSession,
    subject_name: CreateSubject,
) -> JSONResponse:
    subject = Subject(**subject_name.model_dump())
    await session.delete(subject)
    await session.commit()
    return JSONResponse(content={"message": "Entry delete successfully"}, status_code=201)