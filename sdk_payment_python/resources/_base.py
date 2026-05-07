import httpx

from sdk_payment_python.exceptions import KvellAPIError, KvellValidationError
from sdk_payment_python.settings import KvellSettings


class BaseResource:
    def __init__(self, settings: KvellSettings, http: httpx.Client, host: str):
        self._settings = settings
        self._http = http
        self._host = host.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self._host}{path}"

    def _auth_headers(self, signature: str) -> dict:
        return {
            "X-Api-Key": self._settings.get_api_key(),
            "X-Signature": signature,
        }

    def _key_headers(self) -> dict:
        return {"X-Api-Key": self._settings.get_api_key()}

    def _handle_response(self, response: httpx.Response) -> dict:
        if response.status_code == 422:
            raise KvellValidationError(response.json().get("errors", []))
        if response.is_error:
            raise KvellAPIError(response.status_code, response.text)
        return response.json()

    def _post(self, path: str, body: dict, headers: dict) -> dict:
        return self._handle_response(self._http.post(self._url(path), json=body, headers=headers))

    def _get(self, path: str, headers: dict) -> dict:
        return self._handle_response(self._http.get(self._url(path), headers=headers))

    def _get_params(self, path: str, params: dict, headers: dict) -> dict:
        return self._handle_response(self._http.get(self._url(path), params=params, headers=headers))

    def _patch(self, path: str, headers: dict) -> dict:
        return self._handle_response(self._http.patch(self._url(path), headers=headers))

    def _patch_body(self, path: str, body: dict, headers: dict) -> dict:
        return self._handle_response(self._http.patch(self._url(path), json=body, headers=headers))

    def _delete(self, path: str, headers: dict) -> None:
        response = self._http.delete(self._url(path), headers=headers)
        if response.is_error:
            raise KvellAPIError(response.status_code, response.text)


class AsyncBaseResource:
    def __init__(self, settings: KvellSettings, http: httpx.AsyncClient, host: str):
        self._settings = settings
        self._http = http
        self._host = host.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self._host}{path}"

    def _auth_headers(self, signature: str) -> dict:
        return {
            "X-Api-Key": self._settings.get_api_key(),
            "X-Signature": signature,
        }

    def _key_headers(self) -> dict:
        return {"X-Api-Key": self._settings.get_api_key()}

    def _handle_response(self, response: httpx.Response) -> dict:
        if response.status_code == 422:
            raise KvellValidationError(response.json().get("errors", []))
        if response.is_error:
            raise KvellAPIError(response.status_code, response.text)
        return response.json()

    async def _post(self, path: str, body: dict, headers: dict) -> dict:
        return self._handle_response(await self._http.post(self._url(path), json=body, headers=headers))

    async def _get(self, path: str, headers: dict) -> dict:
        return self._handle_response(await self._http.get(self._url(path), headers=headers))

    async def _get_params(self, path: str, params: dict, headers: dict) -> dict:
        return self._handle_response(await self._http.get(self._url(path), params=params, headers=headers))

    async def _patch(self, path: str, headers: dict) -> dict:
        return self._handle_response(await self._http.patch(self._url(path), headers=headers))

    async def _patch_body(self, path: str, body: dict, headers: dict) -> dict:
        return self._handle_response(await self._http.patch(self._url(path), json=body, headers=headers))

    async def _delete(self, path: str, headers: dict) -> None:
        response = await self._http.delete(self._url(path), headers=headers)
        if response.is_error:
            raise KvellAPIError(response.status_code, response.text)
