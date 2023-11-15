from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from core.models import User, Subject



async def add_subjects_by_user(
        session: AsyncSession,
        user: User,
        subjects: list[str],
) -> None:
    stmt_subject = select(Subject).where(Subject.name.in_(subjects))
    subjects = await session.scalars(stmt_subject)

    stmt_user = (
        select(User)
        .where(User.id == user.id)
        .options(
            selectinload(User.subjects)
        )
    )

    user = await session.scalar(stmt_user)

    user.subjects.extend(subjects)
    await session.commit()
