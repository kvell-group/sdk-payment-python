from __future__ import annotations

from sdk_payment_python.models.payout import PayoutCard, PayoutSbp, SbpBank, SbpCheck
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


def _rsa_headers(settings, body: dict) -> dict:
    sig = KvellUtils.create_rsa_signature(settings.get_private_key(), body)
    return {"X-Api-Key": settings.get_api_key(), "X-Signature": sig}


class PayoutsResource(BaseResource):
    def card_create(
        self,
        transaction: str,
        amount: int,
        description: str,
        account_number: str,
        customer_key: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> PayoutCard:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "account_number": account_number,
        }
        if customer_key is not None:
            body["customer_key"] = customer_key
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return PayoutCard.from_dict(self._post("/v1/orders/account2card", body, _rsa_headers(self._settings, body)))

    def card_confirm(self, transaction: str, otp: str) -> PayoutCard:
        body = {"transaction": transaction, "otp": otp}
        return PayoutCard.from_dict(
            self._post("/v1/orders/account2card/confirm", body, _rsa_headers(self._settings, body))
        )

    def sbp_banks(self) -> list[SbpBank]:
        data = self._get("/v1/collections/banks", self._key_headers())
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    def sbp_phone_banks(self, phone: str) -> list[SbpBank]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [phone])
        data = self._get(f"/v1/orders/payout/sbp/banks/{phone}", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    def sbp_check(self, phone: str, bank_id: str) -> SbpCheck:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [phone, bank_id]
        )
        body = {"phone": phone, "bank_id": bank_id}
        return SbpCheck.from_dict(self._post("/v1/orders/payout/sbp/check", body, self._auth_headers(sig)))

    def sbp_create(
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
        return PayoutSbp.from_dict(self._post("/v1/orders/payout/sbp", body, _rsa_headers(self._settings, body)))

    def sbp_confirm(self, transaction: str, otp: str) -> PayoutSbp:
        body = {"transaction": transaction, "otp": otp}
        return PayoutSbp.from_dict(
            self._post("/v1/orders/payout/sbp/confirm", body, _rsa_headers(self._settings, body))
        )


class AsyncPayoutsResource(AsyncBaseResource):
    async def card_create(
        self,
        transaction: str,
        amount: int,
        description: str,
        account_number: str,
        customer_key: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
    ) -> PayoutCard:
        body: dict = {
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "account_number": account_number,
        }
        if customer_key is not None:
            body["customer_key"] = customer_key
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        return PayoutCard.from_dict(
            await self._post("/v1/orders/account2card", body, _rsa_headers(self._settings, body))
        )

    async def card_confirm(self, transaction: str, otp: str) -> PayoutCard:
        body = {"transaction": transaction, "otp": otp}
        return PayoutCard.from_dict(
            await self._post("/v1/orders/account2card/confirm", body, _rsa_headers(self._settings, body))
        )

    async def sbp_banks(self) -> list[SbpBank]:
        data = await self._get("/v1/collections/banks", self._key_headers())
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    async def sbp_phone_banks(self, phone: str) -> list[SbpBank]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [phone])
        data = await self._get(f"/v1/orders/payout/sbp/banks/{phone}", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [SbpBank.from_dict(item) for item in items]

    async def sbp_check(self, phone: str, bank_id: str) -> SbpCheck:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [phone, bank_id]
        )
        body = {"phone": phone, "bank_id": bank_id}
        return SbpCheck.from_dict(await self._post("/v1/orders/payout/sbp/check", body, self._auth_headers(sig)))

    async def sbp_create(
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
        return PayoutSbp.from_dict(await self._post("/v1/orders/payout/sbp", body, _rsa_headers(self._settings, body)))

    async def sbp_confirm(self, transaction: str, otp: str) -> PayoutSbp:
        body = {"transaction": transaction, "otp": otp}
        return PayoutSbp.from_dict(
            await self._post("/v1/orders/payout/sbp/confirm", body, _rsa_headers(self._settings, body))
        )
