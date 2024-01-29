import asyncio
from typing import AsyncGenerator, Any

import pytest
from httpx import AsyncClient, Response

from main import app
from core.config import MODE
from core.db_helper import db_helper
from core.models import Base, Profile
from tests.common.user_authentication_fixture import (
    user_customer_data,
    user_tutor_data,
    register_tutor,
    register_customer,
    auth_headers_tutor,
    auth_headers_customer,
    auth_customer,
    auth_tutor,
)
from tests.common.fixture_profile_management import (
    get_profile,
    create_profile_by_tutor,
    delete_profile,
)


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







