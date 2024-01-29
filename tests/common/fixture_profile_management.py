from typing import Any

import pytest

from api_v1.profile import crud
from api_v1.profile.schemas import CreateProfile
from core import db_helper
from core.models import Profile


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
        description='Я Петров'
    )

    if not get_profile:
        async with db_helper.session_factory() as session:
            await crud.create_profile(
                profile=profile,
                session=session,
                user_id=register_tutor['id'],
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