from typing import Any

from httpx import Response
from fastapi import status

from tests.conftest import BaseRequestAPI

class TestGetSubject(BaseRequestAPI):

    _url = '/user/get_subjects_by_user'
    _method = 'get'

    async def request_by_api(self, headers: dict[str, Any] = None) -> Response:
        return await super().request_by_api(headers=headers)


    async def test_by_tutor(self, auth_headers_tutor, add_subject_by_tutor):
        """Проверка получения репетитором, предметов, которые он ведет"""
        response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_200_OK
