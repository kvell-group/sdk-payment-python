from __future__ import annotations

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class RefundsResource(BaseResource):
    def create(self, transaction: str, amount: int | None = None) -> Transaction:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {}
        if amount is not None:
            body["amount"] = amount
        return Transaction.from_dict(self._post(f"/v1/orders/{transaction}/refund", body, self._auth_headers(sig)))


class AsyncRefundsResource(AsyncBaseResource):
    async def create(self, transaction: str, amount: int | None = None) -> Transaction:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        body: dict = {}
        if amount is not None:
            body["amount"] = amount
        return Transaction.from_dict(
            await self._post(f"/v1/orders/{transaction}/refund", body, self._auth_headers(sig))
        )