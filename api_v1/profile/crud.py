from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateProfile, UpdateProfile

from core.models import Profile, User


async def create_profile(
        session: AsyncSession,
        profile: CreateProfile,
        user_id: int,
) -> Profile:
    profile = Profile(
        user_id=user_id,
        **profile.model_dump()
    )
    session.add(profile)
    await session.commit()
    return profile


async def get_profile(
        user: User,
        session: AsyncSession,
) -> Profile:
    stmt = select(Profile).where(Profile.user_id == user.id)
    profile = await session.execute(stmt)
    profile = profile.scalar()
    return profile


async def update_profile(
        session: AsyncSession,
        profile_update: UpdateProfile,
        profile: Profile,
) -> Profile:
    for name, value in profile_update.model_dump(exclude_unset=True).items():
        setattr(profile, name, value)
    await session.commit()
    return profile


async def delete_profile(
        session: AsyncSession,
        profile: Profile,
) -> None:
    await session.delete(profile)
    await session.commit()



