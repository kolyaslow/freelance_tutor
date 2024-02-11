from typing import Any

from httpx import Response
from fastapi import status
from tests.conftest import BaseRequestAPI


class TestDeleteProfile(BaseRequestAPI):

    _url = "/profile/delete_profile"
    _method = "delete"

    async def test_by_tutor(self, auth_headers_tutor, create_profile_by_tutor):
        """Проверка возможности удалить профиль для репетитора."""
        response: Response = await self.request_by_api(
            headers=auth_headers_tutor,
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    async def test_repeated_delete(self, auth_headers_tutor, delete_profile):
        """Проверка удаления несуществующего профиля."""
        response: Response = await self.request_by_api(
            headers=auth_headers_tutor,
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
