from typing import Any

from httpx import Response
from fastapi import status

from tests.conftest import BaseRequestAPI


class TestShowTutorBySubject(BaseRequestAPI):
    """Првоерка получения профилей всех репетиторов, которые ведут определенный предмет"""

    _subject_name = "informatics"
    _url = f"/user/show_all_tutor_by_subject/{_subject_name}"
    _method = "get"

    async def request_by_api(self, headers: dict[str, Any] = None) -> Response:
        return await super().request_by_api(headers=headers)

    async def test_by_tutor(self, auth_headers_tutor, add_subject_by_tutor):
        "Проверка работы API для репетитора"
        response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_200_OK

    async def test_by_customer(self, auth_headers_customer, add_subject_by_tutor):
        "Проверка работы API для ученика"
        response = await self.request_by_api(headers=auth_headers_customer)
        assert response.status_code == status.HTTP_200_OK

    async def test_wrong_subject(self, auth_headers_tutor):
        """Проверка на передачу несуществующего предмета"""
        self._subject_name = "история"
        response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() in (
            [],
            [{"description": None, "fullname": None}],
        )
