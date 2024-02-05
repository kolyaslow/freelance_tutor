from fastapi import status

from core.models import Order, Subject
from tests.conftest import BaseRequestAPI


class TestDeleteOrder(BaseRequestAPI):

    _url = None
    _method = 'delete'


    async def test_by_customer(
        self,
        auth_headers_customer: dict,
        create_order: Order,
        create_subject: Subject,
    ):
        self._url = f'/order/delete_order/{create_order.id}'

        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status.HTTP_204_NO_CONTENT


    async def test_repeat_delete(
            self,
            delete_order: None,
            auth_headers_customer: dict,
            order: Order,
    ):
        self._url = f'/order/delete_order/{order.id}'
        request = await self.request_by_api(
            headers=auth_headers_customer
        )
        assert request.status_code == status.HTTP_404_NOT_FOUND
