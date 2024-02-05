from tests.conftest import BaseRequestAPI
from fastapi import status
import pytest

from core.models import Order


class TestCreateOrder(BaseRequestAPI):

    _url = '/order/create_order'
    _method = 'post'
    _json = {
        'subject_name': 'informatics',
    }

    @pytest.mark.parametrize(
        'description, is_active, status',
        [
            ('Первый заказ', True, status.HTTP_201_CREATED,),
            ('Первый заказ', False, status.HTTP_201_CREATED,),
            (None, True, status.HTTP_422_UNPROCESSABLE_ENTITY),
            (None, False, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ]
    )
    async def test_by_customer(
        self,
        auth_headers_customer,
        create_subject,
        description,
        is_active,
        status,
    ):
        """Проверка на доступность APi на создание заказа для role=customer"""

        self._json['description'] = description
        self._json['is_active'] = is_active
        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status


    async def test_recreating_order(
        self,
        create_order: Order,
        auth_headers_customer: dict,
        create_subject,
        order: Order,
    ):
        """Проверка на успешное создание повторного заказа"""
        self._json = {
            'description': order.description,
            'is_activ': order.is_active,
            'subject_name': order.subject_name,
        }

        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status.HTTP_201_CREATED



    