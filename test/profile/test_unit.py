import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_profile(client: AsyncClient, auth_tutor: str):
    profile =  {
        'fullname': 'Артемов Артем Артемович',
        'description': 'Я артем'
    }

    headers = {"Authorization": f"Bearer {auth_tutor}"}

    response = await client.post('/profile/create_profile', json=profile, headers=headers)

    assert response.status_code == 201

    assert response.json() == {
        'fullname': 'Артемов Артем Артемович',
        'description': 'Я артем',
    }

