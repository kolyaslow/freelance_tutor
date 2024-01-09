import pytest
from httpx import AsyncClient
from fastapi import status

@pytest.fixture()
def profile_data():
    profile = {
        'fullname': 'Артемов Артем Артемович',
        'description': 'Я артем'
    }

    return profile


class TestCreateProfile():
    async def test_create_profile_by_tutor(
            self,
            client: AsyncClient,
            auth_tutor: str,
            profile_data
    ):
        """Профиль могут содать только репетиторы."""

        headers = {"Authorization": f"Bearer {auth_tutor}"}
        response = await client.post('/profile/create_profile', json=profile_data, headers=headers)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json() == profile_data


    async def test_create_profile_2(
            self,
            client: AsyncClient,
            auth_customer: str,
            profile_data
    ):

        headers = {"Authorization": f"Bearer {auth_customer}"}
        response = await client.post('/profile/create_profile', json=profile_data, headers=headers)

        assert response.status_code == status.HTTP_403_FORBIDDEN





