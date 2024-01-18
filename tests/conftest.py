import asyncio
from typing import AsyncGenerator, Any

import pytest
from httpx import AsyncClient, Response

from api_v1.profile import crud
from api_v1.profile.schemas import CreateProfile
from main import app
from core.config import MODE
from core.db_helper import db_helper
from core.models import Base, Profile


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    """Deleting and creating tables for each tests case."""
    if MODE == 'TEST':
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
        async with db_helper.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for each tests case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

#=======================User Authentication Unit=======================
@pytest.fixture(scope="session")
def user_tutor_data():
    user_data = {
            "email": "user1@example.com",
            "password": "1234",
            "role": "tutor"
    }
    return user_data


@pytest.fixture(scope="session")
def user_customer_data():
    user_data = {
        "email": "user2@example.com",
        "password": "1234",
        "role": "customer"
    }
    return user_data


@pytest.fixture(autouse=True, scope='session')
async def register_tutor(client: AsyncClient, user_tutor_data):
    """Регистрация пользователя с провми репетитора"""
    response = await client.post('/auth/register', json=user_tutor_data)
    return response.json()


@pytest.fixture(autouse=True, scope='session')
async def register_customer(client: AsyncClient, user_customer_data):
    """Регистрация пользователя с правми ученика"""
    response = await client.post('/auth/register', json=user_customer_data)
    return response.json()


@pytest.mark.usefixtures('prepare_database', 'register_tutor')
@pytest.fixture(scope='session')
async def auth_tutor(client: AsyncClient, user_tutor_data) -> str:

    response = await client.post("/auth/jwt/login", data={
        "username": user_tutor_data["email"],
        "password": user_tutor_data["password"],
    })

    token = response.json()['access_token']
    return token


@pytest.mark.usefixtures('prepare_database', 'register_customer')
@pytest.fixture(scope='session')
async def auth_customer(client: AsyncClient, user_customer_data) -> str:

    response = await client.post("/auth/jwt/login", data={
        "username": user_customer_data["email"],
        "password": user_customer_data["password"],
    })
    token = response.json()['access_token']
    return token


@pytest.fixture(scope="session")
def auth_headers_tutor(auth_tutor):
    headers = {"Authorization": f"Bearer {auth_tutor}"}
    return headers

@pytest.fixture(scope="session")
def auth_headers_customer(auth_customer):
    headers = {"Authorization": f"Bearer {auth_customer}"}
    return headers


#==========================Request======================
class BaseRequestAPI:
    """
    Отправка запросов к API

    **Parameters:**

    * **_url** -  адрес API ресурса
    * **_method** -  метод HTTP: GET, POST, DELETE...
    * **_data** - *(optional)* данные тела запроса
    * **_json** - *(optional)* входные данные необходные для запроса в формати json
    """

    _url: str
    _method: str
    _data: dict[str, Any] = None
    _json: dict[str, Any] = None

    async def request_by_api(self, headers: dict[str, Any] = None) -> Response:
        async with AsyncClient(app=app, base_url="http://test") as client:
            request = client.build_request(
                url=self._url,
                method=self._method,
                data=self._data,
                json=self._json,
                headers=headers,
            )

            response: Response = await client.send(request)

            return response





@pytest.fixture
async def get_profile(
        register_tutor: dict[str, Any],
) -> Profile | None:
    """Получения  профиля для репетитора"""
    async with db_helper.session_factory() as session:
        profile = await crud.get_profile(user_id=register_tutor['id'], session=session)

    if profile:
        return profile

    return None


#========================Работа с профилем на уровне БД=====================
@pytest.fixture
async def create_profile_by_tutor(
    register_tutor: dict[str, Any],
    get_profile: Profile | None,
) -> None:
    """Создание профиля репетитора перед тетом"""

    profile = CreateProfile(
        fullname='Петров Степан Стпанович',
        description='Я Петров'
    )

    if not get_profile:
        async with db_helper.session_factory() as session:
            await crud.create_profile(
                profile=profile,
                session=session,
                user_id=register_tutor['id'],
            )


@pytest.fixture
async def delete_profile(
    get_profile: Profile | None,
) -> None:
    """Удаление профиля репетитора перед тестом"""
    if get_profile:
        async with db_helper.session_factory() as session:
            await crud.delete_profile(
                profile=get_profile,
                session=session,
            )

