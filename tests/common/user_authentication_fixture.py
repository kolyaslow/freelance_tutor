import pytest
from httpx import AsyncClient


@pytest.fixture(scope="session")
def user_tutor_data():
    user_data = {
            "email": "tutor@example.com",
            "password": "1234",
            "role": "tutor"
    }
    return user_data


@pytest.fixture(scope="session")
def user_customer_data():
    user_data = {
        "email": "customer@example.com",
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
