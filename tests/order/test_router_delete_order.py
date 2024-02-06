from fastapi import status
import pytest

from core.models import Order, Subject
from tests.conftest import BaseRequestAPI


class TestDeleteOrder(BaseRequestAPI):

    _url = None
    _method = 'delete'


    @pytest.mark.usefixtures('create_subject')
    async def test_by_customer(
        self,
        auth_headers_customer: dict,
        create_order: Order,
    ):
        """Проверка работы Api для пользователя role==customer"""
        self._url = f'/order/delete_order/{create_order.id}'

        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status.HTTP_204_NO_CONTENT


    @pytest.mark.usefixtures('delete_order')
    async def test_deleting_defunct_order(
            self,
            auth_headers_customer: dict,
            order: Order,
    ):
        """Проверка удаления несуществующего заказа"""
        self._url = f'/order/delete_order/{order.id}'
        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
