from __future__ import annotations

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class RecurringResource(BaseResource):
    def rebill(
        self,
        parent_transaction: str,
        transaction: str,
        amount: int,
        description: str,
        fiscal_data: dict | None = None,
        extra_data: dict | None = None,
    ) -> Transaction:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body: dict = {
            "parent_transaction": parent_transaction,
            "transaction": transaction,
            "amount": amount,
            "description": description,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        return Transaction.from_dict(self._post("/v1/orders/rebill", body, self._auth_headers(sig)))

    def rebill_from_profile(
        self,
        parent_transaction: str,
        transaction: str,
        amount: int,
        description: str,
        customer_key: str,
        fiscal_data: dict | None = None,
        extra_data: dict | None = None,
    ) -> Transaction:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body: dict = {
            "parent_transaction": parent_transaction,
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "customer_key": customer_key,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        return Transaction.from_dict(self._post("/v1/orders/rebill-from-profile", body, self._auth_headers(sig)))


class AsyncRecurringResource(AsyncBaseResource):
    async def rebill(
        self,
        parent_transaction: str,
        transaction: str,
        amount: int,
        description: str,
        fiscal_data: dict | None = None,
        extra_data: dict | None = None,
    ) -> Transaction:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body: dict = {
            "parent_transaction": parent_transaction,
            "transaction": transaction,
            "amount": amount,
            "description": description,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        return Transaction.from_dict(await self._post("/v1/orders/rebill", body, self._auth_headers(sig)))

    async def rebill_from_profile(
        self,
        parent_transaction: str,
        transaction: str,
        amount: int,
        description: str,
        customer_key: str,
        fiscal_data: dict | None = None,
        extra_data: dict | None = None,
    ) -> Transaction:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body: dict = {
            "parent_transaction": parent_transaction,
            "transaction": transaction,
            "amount": amount,
            "description": description,
            "customer_key": customer_key,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        return Transaction.from_dict(
            await self._post("/v1/orders/rebill-from-profile", body, self._auth_headers(sig))
        )