from __future__ import annotations

from sdk_payment_python.models.session import AlfaPayResult, SessionCreated, SbpResult
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class SessionResource(BaseResource):
    def create(
        self,
        amount: int,
        transaction: str,
        description: str,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> SessionCreated:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body: dict = {"amount": amount, "transaction": transaction, "description": description}
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if split_data is not None:
            body["split_data"] = split_data
        return SessionCreated.from_dict(self._post("/v1/orders/session", body, self._auth_headers(sig)))

    def sbp(self, transaction: str, customer: str | None = None) -> SbpResult:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {"transaction": transaction}
        if customer is not None:
            body["customer"] = customer
        return SbpResult.from_dict(self._post("/v1/orders/sbp", body, self._auth_headers(sig)))

    def alfapay(self, transaction: str, ip: str, customer: str | None = None) -> AlfaPayResult:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {"transaction": transaction, "ip": ip}
        if customer is not None:
            body["customer"] = customer
        return AlfaPayResult.from_dict(self._post("/v1/orders/alfapay", body, self._auth_headers(sig)))

    def sbp_b2b(self, transaction: str, customer: str | None = None) -> SbpResult:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {"transaction": transaction}
        if customer is not None:
            body["customer"] = customer
        return SbpResult.from_dict(self._post("/v1/orders/sbp/b2b", body, self._auth_headers(sig)))


class AsyncSessionResource(AsyncBaseResource):
    async def create(
        self,
        amount: int,
        transaction: str,
        description: str,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> SessionCreated:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body: dict = {"amount": amount, "transaction": transaction, "description": description}
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if split_data is not None:
            body["split_data"] = split_data
        return SessionCreated.from_dict(await self._post("/v1/orders/session", body, self._auth_headers(sig)))

    async def sbp(self, transaction: str, customer: str | None = None) -> SbpResult:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {"transaction": transaction}
        if customer is not None:
            body["customer"] = customer
        return SbpResult.from_dict(await self._post("/v1/orders/sbp", body, self._auth_headers(sig)))

    async def alfapay(self, transaction: str, ip: str, customer: str | None = None) -> AlfaPayResult:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {"transaction": transaction, "ip": ip}
        if customer is not None:
            body["customer"] = customer
        return AlfaPayResult.from_dict(await self._post("/v1/orders/alfapay", body, self._auth_headers(sig)))

    async def sbp_b2b(self, transaction: str, customer: str | None = None) -> SbpResult:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {"transaction": transaction}
        if customer is not None:
            body["customer"] = customer
        return SbpResult.from_dict(await self._post("/v1/orders/sbp/b2b", body, self._auth_headers(sig)))
