from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, delete
from sqlalchemy.orm import selectinload

from core.models import User, Subject, Profile


async def add_subjects_by_user(
    session: AsyncSession,
    user_id: int,
    subjects: list[str],
) -> None:
    stmt_subject = select(Subject).where(Subject.name.in_(subjects))
    subjects = await session.scalars(stmt_subject)

    stmt_user = (
        select(User).options(selectinload(User.subjects)).where(User.id == user_id)
    )

    user = await session.scalar(stmt_user)

    user.subjects.extend(subjects)
    await session.commit()


async def get_subjects_by_user(
    session: AsyncSession,
    user: User,
) -> list[str]:
    """Запрос на получение всех предметов у репетитора"""
    stmt = select(Subject.name).join(Subject.users).where(User.id == user.id)
    subject_name = await session.scalars(stmt)
    return list(subject_name)


async def show_all_tutor_by_subject(
    session: AsyncSession,
    subject_name: str,
):
    stmt = (
        select(Profile.fullname, Profile.description)
        .join(User.subjects)
        .join(User.profile)
        .where(Subject.name == subject_name)
    )

    result: Result = await session.execute(stmt)
    profiles = result.fetchall()

    return profiles


async def delete_tutor_subjects(
    session: AsyncSession,
    subjects_in: list[str],
    user_id: int,
):

    stmt_get = (
        select(User).options(selectinload(User.subjects)).where(User.id == user_id)
    )
    user: User = await session.scalar(stmt_get)
    for subject in user.subjects:
        if subject.name in subjects_in:
            user.subjects.remove(subject)
    await session.commit()
