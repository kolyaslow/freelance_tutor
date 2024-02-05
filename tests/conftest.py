import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from main import app
from core.config import settings
from core.db_helper import db_helper
from core.models import Base

from tests.common import (
    user_customer_data,
    user_tutor_data,
    register_tutor,
    register_customer,
    auth_headers_tutor,
    auth_headers_customer,
    auth_customer,
    auth_tutor,
    get_profile,
    create_profile_by_tutor,
    delete_profile,
    create_subject,
    BaseRequestAPI,
)


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    """Deleting and creating tables for each tests case."""
    if settings.db.MODE == 'DEV':
        pytest.exit("run only in TEST mode")

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


@pytest.fixture
async def session():
    async with db_helper.session_factory() as session:
        yield session






