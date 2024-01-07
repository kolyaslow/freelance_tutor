from typing import AsyncGenerator

import pytest
from httpx import AsyncClient

from main import app
from core.config import MODE
from core.db_helper import db_helper
from core.models import Base


@pytest.fixture(scope='session')
async def prepare_database():
    """Deleting and creating tables for each test case."""
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


@pytest.fixture
async def register_tutor(user_tutor_data):
    await client.post('/auth/register', json=user_tutor_data)


@pytest.fixture
async def register_customer(user_customer_data):
    await client.post('/auth/register', json=user_customer_data)


@pytest.mark.usefixtures('prepare_database')
@pytest.fixture(scope='session')
async def auth_tutor(client: AsyncClient, user_tutor_data) -> str:

        response = await client.post("/auth/jwt/login", data={
            "username": user_tutor_data["email"],
            "password": user_tutor_data["password"],
        })

        token = response.json()['access_token']

        return token


@pytest.mark.usefixtures('prepare_database')
@pytest.fixture(scope='session')
async def auth_customer(client: AsyncClient, user_customer_data) -> str:

    response = await client.post("/auth/jwt/login", data={
        "username": user_customer_data["email"],
        "password": user_customer_data["password"],
    })

    token = response.json()['access_token']

    return token











