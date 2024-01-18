from typing import Any

import pytest
from httpx import Response
from fastapi import status
from tests.conftest import BaseRequestAPI


class TestUpdateProfile(BaseRequestAPI):

    _url = '/profile/update_profile'
    _method = 'patch'
    _json = None

    async def request_by_api(self, headers: dict[str, Any] = None) -> Response:
        return await super().request_by_api(headers=headers)

    @pytest.mark.parametrize('profile_data',
        [
            {
                'fullname': 'Петров Степан Стпанович',
                'description': 'Я Петров'
            },
            {
                'fullname': 'Петров Степан Стпанович',
                'description': None,
            },
            {
                'fullname': None,
                'description': 'Я Петров'
            },
            {
                'fullname': None,
                'description': None,
            },
        ]
    )
    async def test_by_tutor(self, auth_tutor, create_profile_by_tutor, profile_data):
        """Проверка возможности обновления профиля для репетиторов."""
        self._json = profile_data
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_tutor}"},
        )
        assert response.status_code == status.HTTP_200_OK

    async def test_by_customer(self, auth_customer):
        """Проверка недоступности API для ученика."""
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_customer}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN