from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, APIRouter

from ..user.dependencies import current_user
from . import crud
from .schemas import CreateProfile

if TYPE_CHECKING:
    from core.models import User, Profile

router = APIRouter()

@router.post('/', response_model=Profile)
async def create_profile(
    profile: CreateProfile,
    session: AsyncSession,
    user: User = Depends(current_user.get_current_user()),
) -> Profile:
    return await crud.create_profile(
        session=session,
        user_id=user.id,
        profile=profile,
    )