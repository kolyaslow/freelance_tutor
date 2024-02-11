from typing import Any

import pytest
from fastapi import status
from httpx import Response

from tests.conftest import BaseRequestAPI


class TestCreateProfile(BaseRequestAPI):
    """
    Проверка API по созданию профиля
    """

    _url = "/profile/create_profile"
    _method = "post"
    _json = None

    @pytest.mark.parametrize(
        "fullname",
        [
            "Петров Степан Стпанович",
            None,
        ],
    )
    @pytest.mark.parametrize(
        "description",
        [
            "Я Петров",
            None,
        ],
    )
    async def test_valid_data_by_tutor(
        self, auth_headers_tutor: dict[str, Any], delete_profile, fullname, description
    ):
        """Проверка работы API для пользователя role=tutor"""

        self._json = {
            "fullname": fullname,
            "description": description,
        }
        response: Response = await self.request_by_api(
            headers=auth_headers_tutor,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._json

    async def test_recreate_profile(self, create_profile_by_tutor, auth_headers_tutor):
        response = await self.request_by_api(headers=auth_headers_tutor)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
