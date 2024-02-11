from typing import Any

import pytest
from httpx import Response
from fastapi import status
from tests.conftest import BaseRequestAPI


class TestUpdateProfile(BaseRequestAPI):

    _url = "/profile/update_profile"
    _method = "patch"
    _json = None

    @pytest.mark.parametrize(
        "fullname",
        [
            "Петров Степан Стпанович",
            None,
        ],
    )
    @pytest.mark.parametrize(
        "description",
        [
            "Я Петров",
            None,
        ],
    )
    async def test_valid_data_by_tutor(
        self, auth_headers_tutor, create_profile_by_tutor, fullname, description
    ):
        """Проверка возможности обновления профиля для репетиторов."""
        self._json = {
            "fullname": fullname,
            "description": description,
        }
        response: Response = await self.request_by_api(
            headers=auth_headers_tutor,
        )
        assert response.status_code == status.HTTP_200_OK
