import pytest
from fastapi import status
from httpx import Response

from tests.conftest import BaseRequestAPI


class TestsAccessRights(BaseRequestAPI):
    """
    Проверка недоступности API для пользователей с разними правами
    """

    _method = None
    _url = None

    @pytest.mark.parametrize(
        "method, url",
        [
            ("post", "/profile/create_profile"),
            ("delete", "/profile/delete_profile"),
            ("patch", "/profile/update_profile"),
            ("get", "/user/get_subjects_by_user"),
            ("post", "/user/add_subject"),
            ("post", "subject/create_subject"),
            ("delete", "subject/delete_subject/informatics"),
        ],
    )
    async def test_inaccessibility_api_by_customer(
        self,
        auth_headers_customer,
        method,
        url,
    ):
        self._method = method
        self._url = url
        response: Response = await self.request_by_api(headers=auth_headers_customer)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.parametrize(
        "method, url",
        [
            ("post", "order/create_order"),
            ("delete", "order/delete_order/1"),
            ("post", "subject/create_subject"),
            ("delete", "subject/delete_subject/informatics"),
        ],
    )
    async def test_inaccessibility_api_by_tutor(
        self,
        auth_headers_tutor,
        method,
        url,
    ):
        self._method = method
        self._url = url
        response: Response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_403_FORBIDDEN
