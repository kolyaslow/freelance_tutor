import pytest
from httpx import Response
from fastapi import status

from tests.conftest import BaseRequestAPI


class TestInaccessibility(BaseRequestAPI):
    """
    Проверка недустопности API для определенной роли

    **Список недоступных API для role=customer:**
        *API связанные с профилем(удаление, создание, обновление),\n
        *API связанные с предметом(
            получение всех предметов репетитора,
            добавление пердмета пользователю,
        )\n



    """

    _method = None
    _url = None


    @pytest.mark.parametrize(
        'method, url',
        [
            ('post','/profile/create_profile'),
            ('delete', '/profile/delete_profile'),
            ('patch', '/profile/update_profile'),
            ('get', '/user/get_subjects_by_user'),
            ('post', '/user/add_subject')
        ]
    )
    async def test_inaccessibility_by_customer(self, auth_headers_customer, method, url):
        self._method = method
        self._url = url
        response: Response = await self.request_by_api(
            headers=auth_headers_customer
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN