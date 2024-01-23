from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.orm import selectinload

from api_v1.profile.schemas import ReadProfile
from core.models import User, Subject, Profile



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


async def get_subjects_by_user(
        session: AsyncSession,
        user: User,
) -> list[str]:
    stmt = (
        select(Subject)
        .join(Subject.users)
        .where(User.id == user.id)
    )
    subjects = await session.scalars(stmt)
    subject_by_user = [res.name for res in subjects]
    return subject_by_user


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
