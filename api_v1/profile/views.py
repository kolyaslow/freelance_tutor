from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter, status, HTTPException

from ..user.dependencies import checking_tutor
from . import crud
from .schemas import CreateProfile, UpdateProfile
from core.db_helper import db_helper
from core.models import User, Profile
from .dependencies import get_profile


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


# @router.patch('/update_profile')
# async def update_profile(
#         profile_update: UpdateProfile,
#         session: AsyncSession = Depends(db_helper.session_dependency),
#         user: User = Depends(checking_tutor)
# ) -> UpdateProfile:



@router.delete('/delete_profile',  status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(checking_tutor)])
async def delete_profile(
        session: AsyncSession = Depends(db_helper.session_dependency),
        profile: Profile = Depends(get_profile),
) -> None:
    await crud.delete_profile(session=session, profile=profile)




