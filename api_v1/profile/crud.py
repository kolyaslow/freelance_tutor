from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import CreateProfile



from core.models import Profile

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