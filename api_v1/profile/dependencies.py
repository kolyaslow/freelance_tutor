from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core import db_helper
from core.models import Profile, User

from ..common.dependencies import user_rights
from . import crud


async def get_profile(
    user: User = Depends(user_rights.checking_tutor),
    session: AsyncSession = Depends(db_helper.session_dependency),
) -> Profile:
    profile = await crud.get_profile(user_id=user.id, session=session)

    if profile:
        return profile

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No profile was found for user {user.email}",
    )
