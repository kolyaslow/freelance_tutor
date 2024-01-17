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
    async def test_by_tutor(self, auth_tutor: str, profile_data, delete_profile):
        """Проверка на создание профиля для репетиторов"""

        self._json = profile_data
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_tutor}"},
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == self._json


    async def test_by_customer(self, auth_customer: str):
        """ Проверка на недоступность API для ученика"""
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_customer}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN


    async def test_recreate_profile(self, create_profile_by_tutor, auth_tutor):
        request = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_tutor}"}
        )

        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteProfile(BaseRequestAPI):

    _url = '/profile/delete_profile'
    _method = 'delete'

    async def request_by_api(self, headers: dict[str, Any] = None) -> Response:
        return await super().request_by_api(headers=headers)


    async def test_by_tutor(self, auth_tutor, create_profile_by_tutor):
        """Проверка возможности удалить профиль для репетитора."""
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_tutor}"},
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
#
    async def test_by_customer(self, auth_customer):
        """Проверка недоступности API для ученика."""
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_customer}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    async def test_repeated_delete(self, auth_tutor, delete_profile):
        """Проверка удаления несуществующего профиля."""
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_tutor}"},
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND


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
        """Проверка недоступности API для ученика ."""
        response: Response = await self.request_by_api(
            headers={"Authorization": f"Bearer {auth_customer}"},
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN