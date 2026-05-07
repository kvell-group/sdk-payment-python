from __future__ import annotations

from sdk_payment_python.models.invoice import Invoice
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class InvoicesResource(BaseResource):
    def create(
        self,
        invoice_number: str,
        amount: int,
        description: str,
        delivery_type: str | None = None,
        delivery_value: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> Invoice:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [invoice_number, amount]
        )
        body: dict = {"invoice_number": invoice_number, "amount": amount, "description": description}
        if delivery_type is not None:
            body["delivery_type"] = delivery_type
        if delivery_value is not None:
            body["delivery_value"] = delivery_value
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if split_data is not None:
            body["split_data"] = split_data
        return Invoice.from_dict(self._post("/v1/invoices", body, self._auth_headers(sig)))

    def get(self, invoice_guid: str) -> Invoice:
        return Invoice.from_dict(self._get(f"/v1/invoices/{invoice_guid}", self._key_headers()))

    def cancel(self, invoice_guid: str) -> Invoice:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [invoice_guid])
        return Invoice.from_dict(self._patch(f"/v1/invoices/{invoice_guid}/cancel", self._auth_headers(sig)))


class AsyncInvoicesResource(AsyncBaseResource):
    async def create(
        self,
        invoice_number: str,
        amount: int,
        description: str,
        delivery_type: str | None = None,
        delivery_value: str | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> Invoice:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [invoice_number, amount]
        )
        body: dict = {"invoice_number": invoice_number, "amount": amount, "description": description}
        if delivery_type is not None:
            body["delivery_type"] = delivery_type
        if delivery_value is not None:
            body["delivery_value"] = delivery_value
        if extra_data is not None:
            body["extra_data"] = extra_data
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if split_data is not None:
            body["split_data"] = split_data
        return Invoice.from_dict(await self._post("/v1/invoices", body, self._auth_headers(sig)))

    async def get(self, invoice_guid: str) -> Invoice:
        return Invoice.from_dict(await self._get(f"/v1/invoices/{invoice_guid}", self._key_headers()))

    async def cancel(self, invoice_guid: str) -> Invoice:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [invoice_guid])
        return Invoice.from_dict(await self._patch(f"/v1/invoices/{invoice_guid}/cancel", self._auth_headers(sig)))
