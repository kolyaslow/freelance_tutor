from typing import Any

from httpx import AsyncClient, Response

from main import app


class BaseRequestAPI:
    """
    Формирование и отправка запросов к API

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