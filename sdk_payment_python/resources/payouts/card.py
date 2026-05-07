from __future__ import annotations

from sdk_payment_python.models.payout import PayoutCard
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource


class PayoutsCardResource(BaseResource):
    def create(
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
        return PayoutCard.from_dict(self._post("/v1/orders/account2card", body, self._rsa_headers(body)))

    def confirm(self, transaction: str, otp: str) -> PayoutCard:
        body = {"transaction": transaction, "otp": otp}
        return PayoutCard.from_dict(self._post("/v1/orders/account2card/confirm", body, self._rsa_headers(body)))


class AsyncPayoutsCardResource(AsyncBaseResource):
    async def create(
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
        return PayoutCard.from_dict(await self._post("/v1/orders/account2card", body, self._rsa_headers(body)))

    async def confirm(self, transaction: str, otp: str) -> PayoutCard:
        body = {"transaction": transaction, "otp": otp}
        return PayoutCard.from_dict(await self._post("/v1/orders/account2card/confirm", body, self._rsa_headers(body)))
