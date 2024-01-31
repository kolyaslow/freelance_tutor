from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import Depends, APIRouter, status, HTTPException

from ..common.dependencies import user_rights
from . import crud
from .schemas import CreateProfile, UpdateProfile, ReadProfile
from core.db_helper import db_helper
from core.models import User, Profile
from .dependencies import get_profile
from ..common import crud as crud_common


router = APIRouter()


@router.post('/create_profile', response_model=ReadProfile, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile: CreateProfile,
    session: AsyncSession = Depends(db_helper.session_dependency),
    user: User = Depends(user_rights.checking_tutor),
) -> Profile:
    try:
        profile.user_id = user.id
        return await crud_common.create_db_item(
            session=session,
            model_db=Profile,
            data=profile,
        )
    except IntegrityError:  # обработка повторного создания объекта
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Профиль для пользователя с именем {user.email} уже создан"
        )


@router.patch(
    '/update_profile',
    dependencies=[Depends(user_rights.checking_tutor)],
    response_model=CreateProfile,
)
async def update_profile(
        profile_update: UpdateProfile,
        session: AsyncSession = Depends(db_helper.session_dependency),
        profile: Profile = Depends(get_profile),
) -> Profile:
    return await crud.update_profile(
        profile=profile,
        profile_update=profile_update,
        session=session,
    )

@router.delete(
    '/delete_profile',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(user_rights.checking_tutor)]
)
async def delete_profile(
        session: AsyncSession = Depends(db_helper.session_dependency),
        profile: Profile = Depends(get_profile),
) -> None:
    await crud_common.delete_db_item(
        session=session,
        delete_item=profile
    )





