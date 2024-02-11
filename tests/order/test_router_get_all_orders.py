import pytest
from fastapi import status

from core.models import Order
from tests.conftest import BaseRequestAPI


class TestGetAllOrders(BaseRequestAPI):

    _url = "/order/get_all_orders"
    _method = "get"

    @pytest.mark.usefixtures("create_order", "create_subject")
    async def test_by_customer(
        self,
        auth_headers_customer,
    ):
        """Проверка доступности API для пользователя role=customer"""
        response = await self.request_by_api(headers=auth_headers_customer)
        assert response.status_code == status.HTTP_200_OK
