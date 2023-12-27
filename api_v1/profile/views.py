from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status, HTTPException

from ..user.dependencies import checking_tutor
from . import crud
from .schemas import CreateProfile
from core.db_helper import db_helper
from core.models import User, Profile


router = APIRouter()

@router.post('/create_profile', response_model=CreateProfile)
async def create_profile(
    profile: CreateProfile,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(checking_tutor),
) -> Profile:
    return await crud.create_profile(
        session=session,
        user_id=user.id,
        profile=profile,
    )


@router.delete('/delete_profile', status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
        session: AsyncSession = Depends(db_helper.session_dependency),
        user: User = Depends(checking_tutor)
) -> None | HTTPException:
    return await crud.delete_profile(session=session, user=user)



