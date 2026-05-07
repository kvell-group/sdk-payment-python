from __future__ import annotations

from sdk_payment_python.models.payout import PayoutSbp, SbpBank, SbpCheck, SbpCheckStatus
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class PayoutsSbpResource(BaseResource):
    def banks(self) -> list[SbpBank]:
        data = self._get("/v1/collections/banks", self._key_headers())
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    def phone_banks(self, phone: str) -> list[SbpBank]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [phone])
        data = self._get(f"/v1/orders/payout/sbp/banks/{phone}", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    def check(self, phone: str, bank_id: str) -> SbpCheck:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [phone, bank_id]
        )
        body = {"phone": phone, "bank_id": bank_id}
        return SbpCheck.from_dict(self._post("/v1/orders/payout/sbp/check", body, self._auth_headers(sig)))

    def create(
        self,
        transaction: str,
        amount: int,
        description: str,
        phone: str,
        bank_id: str,
        customer_key: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> PayoutSbp:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "phone": phone,
            "bank_id": bank_id,
        }
        if customer_key is not None:
            body["customer_key"] = customer_key
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return PayoutSbp.from_dict(self._post("/v1/orders/payout/sbp", body, self._rsa_headers(body)))

    def confirm(self, transaction: str, otp: str) -> PayoutSbp:
        body = {"transaction": transaction, "otp": otp}
        return PayoutSbp.from_dict(self._post("/v1/orders/payout/sbp/confirm", body, self._rsa_headers(body)))

    def check_status(self, request_id: str) -> SbpCheckStatus:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [request_id])
        return SbpCheckStatus.from_dict(
            self._get(f"/v1/orders/payout/sbp/check/status/{request_id}", self._auth_headers(sig))
        )


class AsyncPayoutsSbpResource(AsyncBaseResource):
    async def banks(self) -> list[SbpBank]:
        data = await self._get("/v1/collections/banks", self._key_headers())
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    async def phone_banks(self, phone: str) -> list[SbpBank]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [phone])
        data = await self._get(f"/v1/orders/payout/sbp/banks/{phone}", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    async def check(self, phone: str, bank_id: str) -> SbpCheck:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [phone, bank_id]
        )
        body = {"phone": phone, "bank_id": bank_id}
        return SbpCheck.from_dict(await self._post("/v1/orders/payout/sbp/check", body, self._auth_headers(sig)))

    async def create(
        self,
        transaction: str,
        amount: int,
        description: str,
        phone: str,
        bank_id: str,
        customer_key: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> PayoutSbp:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "phone": phone,
            "bank_id": bank_id,
        }
        if customer_key is not None:
            body["customer_key"] = customer_key
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return PayoutSbp.from_dict(await self._post("/v1/orders/payout/sbp", body, self._rsa_headers(body)))

    async def confirm(self, transaction: str, otp: str) -> PayoutSbp:
        body = {"transaction": transaction, "otp": otp}
        return PayoutSbp.from_dict(await self._post("/v1/orders/payout/sbp/confirm", body, self._rsa_headers(body)))

    async def check_status(self, request_id: str) -> SbpCheckStatus:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [request_id])
        return SbpCheckStatus.from_dict(
            await self._get(f"/v1/orders/payout/sbp/check/status/{request_id}", self._auth_headers(sig))
        )
