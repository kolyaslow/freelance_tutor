import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
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


# async def main():
#     async with db_helper.session_factory() as session:
#         await get_subjects_by_user(session=session, user_id=1)
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
