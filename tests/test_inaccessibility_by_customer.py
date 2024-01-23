import pytest
from httpx import Response
from fastapi import status

from conftest import BaseRequestAPI


class TestInaccessibilityByCustomer(BaseRequestAPI):
    """
    Проверка недустопности API для ученика

    Список недоступных API:
        API связанные с профилем(удаление, создание, обновление)

    """

    _method = None
    _url = None


    @pytest.mark.parametrize(
        'method, url',
        [
            ('post','/profile/create_profile'),
            ('delete', '/profile/delete_profile'),
            ('patch', '/profile/update_profile')
        ]
    )
    async def test_inaccessibility_by_customer(self, auth_headers_customer, method, url):
        self._method = method
        self._url = url
        response: Response = await self.request_by_api(
            headers=auth_headers_customer
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN