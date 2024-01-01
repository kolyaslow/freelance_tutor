from typing import TYPE_CHECKING

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateProfile, ProfileUpdate



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


async def update_profile(
        session: AsyncSession,
        profile_update: ProfileUpdate,
) -> ProfileUpdate:
    pass


async def delete_profile(
        user: User,
        session: AsyncSession,
) -> None:
    stmt = select(Profile).where(Profile.user_id == user.id)
    profile = await session.execute(stmt)
    profile = profile.scalar()

    if profile:
        await session.delete(profile)
        await session.commit()



