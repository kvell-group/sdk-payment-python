from __future__ import annotations

from sdk_payment_python.models.smz import InnCheck, SmzClient, SmzReceipt
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class SmzResource(BaseResource):
    def inn_check(self, inn: str) -> InnCheck:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [inn])
        return InnCheck.from_dict(self._get_params("/v1/smz/inn/check", {"inn": inn}, self._auth_headers(sig)))

    def create(
        self,
        inn: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        second_name: str | None = None,
    ) -> SmzClient:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(),
            self._settings.get_secret_key(),
            [inn, first_name, last_name, email, phone],
        )
        body: dict = {
            "inn": inn,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
        }
        if second_name is not None:
            body["second_name"] = second_name
        return SmzClient.from_dict(self._post("/v1/smz/clients", body, self._auth_headers(sig)))

    def receipt_create(
        self,
        inn: str,
        amount: int,
        service_name: str,
        description: str | None = None,
    ) -> SmzReceipt:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [inn, amount])
        body: dict = {"inn": inn, "amount": amount, "service_name": service_name}
        if description is not None:
            body["description"] = description
        return SmzReceipt.from_dict(self._post("/v1/smz/receipts", body, self._auth_headers(sig)))

    def receipt_get(self, receipt_id: int) -> SmzReceipt:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [receipt_id])
        return SmzReceipt.from_dict(self._get(f"/v1/smz/receipts/{receipt_id}", self._auth_headers(sig)))

    def receipt_cancel(self, receipt_id: int) -> SmzReceipt:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [receipt_id])
        return SmzReceipt.from_dict(self._post(f"/v1/smz/receipts/{receipt_id}/cancel", {}, self._auth_headers(sig)))


class AsyncSmzResource(AsyncBaseResource):
    async def inn_check(self, inn: str) -> InnCheck:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [inn])
        return InnCheck.from_dict(await self._get_params("/v1/smz/inn/check", {"inn": inn}, self._auth_headers(sig)))

    async def create(
        self,
        inn: str,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        second_name: str | None = None,
    ) -> SmzClient:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(),
            self._settings.get_secret_key(),
            [inn, first_name, last_name, email, phone],
        )
        body: dict = {
            "inn": inn,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
        }
        if second_name is not None:
            body["second_name"] = second_name
        return SmzClient.from_dict(await self._post("/v1/smz/clients", body, self._auth_headers(sig)))

    async def receipt_create(
        self,
        inn: str,
        amount: int,
        service_name: str,
        description: str | None = None,
    ) -> SmzReceipt:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [inn, amount])
        body: dict = {"inn": inn, "amount": amount, "service_name": service_name}
        if description is not None:
            body["description"] = description
        return SmzReceipt.from_dict(await self._post("/v1/smz/receipts", body, self._auth_headers(sig)))

    async def receipt_get(self, receipt_id: int) -> SmzReceipt:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [receipt_id])
        return SmzReceipt.from_dict(await self._get(f"/v1/smz/receipts/{receipt_id}", self._auth_headers(sig)))

    async def receipt_cancel(self, receipt_id: int) -> SmzReceipt:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [receipt_id])
        return SmzReceipt.from_dict(
            await self._post(f"/v1/smz/receipts/{receipt_id}/cancel", {}, self._auth_headers(sig))
        )
