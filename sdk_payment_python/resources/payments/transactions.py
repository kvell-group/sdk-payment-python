from __future__ import annotations

import uuid

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.settings import KvellSettings
from sdk_payment_python.utils import KvellUtils


class TransactionsResource(BaseResource):
    def __init__(self, settings: KvellSettings, http, host: str, baas_host: str | None = None):
        super().__init__(settings, http, host)
        self._baas_host = (baas_host or host).rstrip("/")

    def _baas_url(self, path: str) -> str:
        return f"{self._baas_host}{path}"

    def get(self, transaction: str) -> Transaction:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        return Transaction.from_dict(self._get(f"/v1/orders/{transaction}", self._auth_headers(sig)))

    def list(
        self,
        page: int = 1,
        size: int = 20,
        status: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[Transaction]:
        request_id = str(uuid.uuid4())
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [request_id])
        headers = {**self._auth_headers(sig), "X-Request-Id": request_id}
        params: dict = {"page": page, "size": size}
        if status is not None:
            params["status"] = status
        if date_from is not None:
            params["date_from"] = date_from
        if date_to is not None:
            params["date_to"] = date_to
        data = self._handle_response(self._http.get(self._baas_url("/v1/orders"), params=params, headers=headers))
        items = data if isinstance(data, list) else data.get("items", [])
        return [Transaction.from_dict(item) for item in items]

    def registry(self, email: str, transactions: list[str] | None = None, orders: list[str] | None = None) -> None:
        body: dict = {"email": email}
        if transactions is not None:
            body["transactions"] = transactions
        if orders is not None:
            body["orders"] = orders
        sig = KvellUtils.create_signature_by_json_body(
            self._settings.get_api_key(), self._settings.get_secret_key(), body
        )
        url = f"{self._baas_host}/v1/registries/transactions/pdf"
        self._handle_response(self._http.post(url, json=body, headers=self._auth_headers(sig)))


class AsyncTransactionsResource(AsyncBaseResource):
    def __init__(self, settings: KvellSettings, http, host: str, baas_host: str | None = None):
        super().__init__(settings, http, host)
        self._baas_host = (baas_host or host).rstrip("/")

    def _baas_url(self, path: str) -> str:
        return f"{self._baas_host}{path}"

    async def get(self, transaction: str) -> Transaction:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        return Transaction.from_dict(await self._get(f"/v1/orders/{transaction}", self._auth_headers(sig)))

    async def list(
        self,
        page: int = 1,
        size: int = 20,
        status: str | None = None,
        date_from: str | None = None,
        date_to: str | None = None,
    ) -> list[Transaction]:
        request_id = str(uuid.uuid4())
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [request_id])
        headers = {**self._auth_headers(sig), "X-Request-Id": request_id}
        params: dict = {"page": page, "size": size}
        if status is not None:
            params["status"] = status
        if date_from is not None:
            params["date_from"] = date_from
        if date_to is not None:
            params["date_to"] = date_to
        data = self._handle_response(await self._http.get(self._baas_url("/v1/orders"), params=params, headers=headers))
        items = data if isinstance(data, list) else data.get("items", [])
        return [Transaction.from_dict(item) for item in items]

    async def registry(
        self, email: str, transactions: list[str] | None = None, orders: list[str] | None = None
    ) -> None:
        body: dict = {"email": email}
        if transactions is not None:
            body["transactions"] = transactions
        if orders is not None:
            body["orders"] = orders
        sig = KvellUtils.create_signature_by_json_body(
            self._settings.get_api_key(), self._settings.get_secret_key(), body
        )
        url = f"{self._baas_host}/v1/registries/transactions/pdf"
        self._handle_response(await self._http.post(url, json=body, headers=self._auth_headers(sig)))
