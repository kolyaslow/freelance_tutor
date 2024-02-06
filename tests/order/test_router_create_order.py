from tests.conftest import BaseRequestAPI
from fastapi import status
import pytest

from core.models import Order


class TestCreateOrder(BaseRequestAPI):
    """Првоерка работы API, для пользователя с role=customer"""
    _url = '/order/create_order'
    _method = 'post'
    _json = None

    async def test_missing_subject_name(self, auth_headers_customer, order: Order):
        self._json = {
            'description': order.description,
            'is_active': order.is_active,
        }
        request = await self.request_by_api(headers=auth_headers_customer)
        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_missing_description(self, auth_headers_customer, order: Order):
        self._json = {
            'subject_name': order.subject_name,
            'is_active': order.is_active,
        }
        request = await self.request_by_api(headers=auth_headers_customer)
        assert request.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_valid_data(
        self,
        auth_headers_customer,
        create_subject,
        order: Order,
    ):
        self._json = {
            'description': order.description,
            'is_active': order.is_active,
            'subject_name': order.subject_name,
        }
        request = await self.request_by_api(headers=auth_headers_customer)
        assert request.status_code == status.HTTP_201_CREATED



    async def test_recreating_order(
        self,
        create_order: Order,
        auth_headers_customer: dict,
        create_subject,
        order: Order,
    ):
        """Проверка создания дубликата заказа"""
        self._json = {
            'description': order.description,
            'is_activ': order.is_active,
            'subject_name': order.subject_name,
        }

        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status.HTTP_201_CREATED



    