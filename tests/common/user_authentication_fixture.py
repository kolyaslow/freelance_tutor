from unittest.mock import patch

import pytest
from httpx import AsyncClient

from api_v1.user import crud as user_crud
from api_v1.user.config import UserManager
from core import db_helper

from . import crud as crud_test


@pytest.fixture(scope="session")
def user_tutor_data():
    user_data = {"email": "tutor@example.com", "password": "1234", "role": "tutor"}
    return user_data


@pytest.fixture(scope="session")
def user_customer_data():
    user_data = {
        "email": "customer@example.com",
        "password": "1234",
        "role": "customer",
    }
    return user_data


@pytest.fixture(autouse=True, scope="session")
async def register_tutor(client: AsyncClient, user_tutor_data):
    """Регистрация пользователя с провми репетитора"""
    with patch.object(UserManager, "on_after_register") as mock_on_after_register:
        mock_on_after_register.return_value = None
        response = await client.post("/auth/register", json=user_tutor_data)
        return response.json()


@pytest.fixture(autouse=True, scope="session")
async def register_customer(client: AsyncClient, user_customer_data):
    """Регистрация пользователя с правми ученика"""
    with patch.object(UserManager, "on_after_register") as mock_on_after_register:
        mock_on_after_register.return_value = None
        response = await client.post("/auth/register", json=user_customer_data)
        return response.json()


async def set_field_verified(user_email: str):
    async with db_helper.session_factory() as session:
        user = await crud_test.get_user_by_email(session=session, email=user_email)

        await user_crud.set_field_verified(session=session, user=user)


@pytest.mark.usefixtures("prepare_database", "register_customer")
@pytest.fixture(autouse=True, scope="session")
async def set_field_verified_by_customer(user_customer_data):
    await set_field_verified(user_customer_data["email"])


@pytest.mark.usefixtures("prepare_database", "register_tutor")
@pytest.fixture(autouse=True, scope="session")
async def set_field_verified_by_tutor(user_tutor_data):
    await set_field_verified(user_tutor_data["email"])


@pytest.mark.usefixtures("prepare_database", "set_field_verified")
@pytest.fixture(scope="session")
async def auth_tutor(client: AsyncClient, user_tutor_data) -> str:

    response = await client.post(
        "/auth/jwt/login",
        data={
            "username": user_tutor_data["email"],
            "password": user_tutor_data["password"],
        },
    )

    token = response.json()["access_token"]
    return token


@pytest.mark.usefixtures("prepare_database", "set_field_verified")
@pytest.fixture(scope="session")
async def auth_customer(client: AsyncClient, user_customer_data) -> str:

    response = await client.post(
        "/auth/jwt/login",
        data={
            "username": user_customer_data["email"],
            "password": user_customer_data["password"],
        },
    )
    token = response.json()["access_token"]
    return token


@pytest.fixture(scope="session")
def auth_headers_tutor(auth_tutor):
    headers = {"Authorization": f"Bearer {auth_tutor}"}
    return headers


@pytest.fixture(scope="session")
def auth_headers_customer(auth_customer):
    headers = {"Authorization": f"Bearer {auth_customer}"}
    return headers
