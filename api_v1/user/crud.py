from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from core.models import User, Subject
from .schemas import UserProfile



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


async def show_user_with_profile(
        session: AsyncSession,
        user: User,
) -> UserProfile:
    stmt = (
        select(User)
        .options(joinedload(User.profile))
        .where(User.id == user.id)
    )
    return  await session.execute(stmt)