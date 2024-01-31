from typing import Any

import pytest

from api_v1.profile import crud
from api_v1.profile.schemas import CreateProfile
from core import db_helper
from core.models import Profile
from api_v1.common import crud as crud_common

@pytest.fixture
async def get_profile(
        register_tutor: dict[str, Any],
) -> Profile | None:
    """Получения  профиля для репетитора"""
    async with db_helper.session_factory() as session:
        profile = await crud.get_profile(user_id=register_tutor['id'], session=session)

    if profile:
        return profile

    return None


@pytest.fixture
async def create_profile_by_tutor(
    register_tutor: dict[str, Any],
    get_profile: Profile | None,
) -> None:
    """Создание профиля репетитора перед тетом"""

    profile = CreateProfile(
        fullname='Петров Степан Стпанович',
        description='Я Петров',
        user_id=register_tutor['id'],
    )

    if get_profile:
        return

    async with db_helper.session_factory() as session:
        await crud_common.create_db_item(
            session=session,
            model_db=Profile,
            data=profile,
        )


@pytest.fixture
async def delete_profile(
    get_profile: Profile | None,
) -> None:
    """Удаление профиля репетитора перед тестом"""
    if get_profile:
        async with db_helper.session_factory() as session:
            await crud.delete_profile(
                profile=get_profile,
                session=session,
            )