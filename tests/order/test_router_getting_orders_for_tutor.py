import pytest
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.user import crud as user_crud
from tests.conftest import BaseRequestAPI


@pytest.fixture
async def delete_all_tutor_subjects(
    session: AsyncSession,
    register_tutor: dict,
):
    """Удаление всех предметов, которые ведет репетитор"""
    subjects = [
        "informatics",
        "mathematics",
        "programming",
    ]

    await user_crud.delete_tutor_subjects(
        session=session, subjects_in=subjects, user_id=register_tutor["id"]
    )


class TestGettingOrdersForTutor(BaseRequestAPI):

    _url = "order/getting_orders_for_tutor"
    _method = "get"

    async def test_valid_data(
        self,
        auth_headers_tutor,
        add_subject_by_tutor,
        create_order,
    ):
        """
        Проверка, что у репиторара есть предметы, которые он ведет,
        а также есть заказы на этот предмет.
        """

        response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_200_OK

    async def test_empty_list_subject(
        self,
        auth_headers_tutor,
        delete_all_tutor_subjects,
    ):
        """Проверка случая, когда репетитор не ведет ни одного предмета"""
        response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    async def test_empty_order(
        self,
        add_subject_by_tutor,
        auth_headers_tutor,
    ):
        """Проверка случая, когда нет подходящих заказов"""
        response = await self.request_by_api(headers=auth_headers_tutor)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    async def test_just_right_orders(
        self,
        add_subject_by_tutor,
        auth_headers_tutor,
        create_order,
    ):
        """Проверка на получение только необходимых заказов"""
        response = await self.request_by_api(headers=auth_headers_tutor)
        assert response.status_code == status.HTTP_200_OK

        for order in response.json():
            assert order["subject_name"] == "informatics"
