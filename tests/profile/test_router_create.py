from typing import Any

import pytest
from httpx import Response
from fastapi import status
from tests.conftest import BaseRequestAPI


class TestCreateProfile(BaseRequestAPI):
    """
    Проверка API по созданию профиля
    """

    _url = '/profile/create_profile'
    _method = 'post'
    _json = None

    async def request_by_api(self, headers: dict[str, Any] = None) -> Response:
        return await super().request_by_api(headers=headers)

    @pytest.mark.parametrize('profile_data',
        [
            {
                'fullname': 'Петров Степан Стпанович',
                'description': 'Я Петров',
            },
            {
                'fullname': 'Петров Степан Стпанович',
                'description': None,
            },
            {
                'fullname': None,
                'description': 'Я Петров',
            },
            {
                'fullname': None,
                'description': None,
            },
        ]
    )
    async def test_by_tutor(self, auth_headers_tutor: dict[str, Any], profile_data, delete_profile):
        """Проверка на создание профиля для репетиторов"""

        self._json = profile_data
        response: Response = await self.request_by_api(
            headers=auth_headers_tutor,
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._json


    async def test_recreate_profile(self, create_profile_by_tutor, auth_headers_tutor):
        request = await self.request_by_api(
            headers=auth_headers_tutor
        )

        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY