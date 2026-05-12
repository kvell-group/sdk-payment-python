from __future__ import annotations

import json
from urllib.parse import urlencode

from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.settings import KvellSettings
from sdk_payment_python.utils import KvellUtils


class _CheckoutMixin:
    _settings: KvellSettings
    _host: str

    def _signature(self, amount: int, transaction: str, expires_at: int | None = None) -> str:
        values: list = [transaction, amount]
        if expires_at is not None:
            values.append(expires_at)
        return KvellUtils.create_signature(
            self._settings.get_api_key(),
            self._settings.get_secret_key(),
            values,
        )

    def _params(
        self,
        amount: int,
        transaction: str,
        description: str,
        success_url: str,
        fail_url: str,
        expires_at: int | None = None,
        phone: str | None = None,
        customer_key: str | None = None,
        auto_return: int | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> dict:
        params: dict = {
            "api_key": self._settings.get_api_key(),
            "amount": amount,
            "transaction": transaction,
            "description": description,
            "success_url": success_url,
            "fail_url": fail_url,
            "signature": self._signature(amount, transaction, expires_at),
        }
        if expires_at is not None:
            params["expires_at"] = expires_at
        if phone is not None:
            params["phone"] = phone
        if customer_key is not None:
            params["customer_key"] = customer_key
        if auto_return is not None:
            params["auto_return"] = auto_return
        if extra_data is not None:
            params["extra_data"] = extra_data
        if fiscal_data is not None:
            params["fiscal_data"] = fiscal_data
        if split_data is not None:
            params["split_data"] = split_data
        return params

    def build_url(
        self,
        amount: int,
        transaction: str,
        description: str,
        success_url: str,
        fail_url: str,
        expires_at: int | None = None,
        phone: str | None = None,
        customer_key: str | None = None,
        auto_return: int | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> str:
        params = self._params(
            amount,
            transaction,
            description,
            success_url,
            fail_url,
            expires_at,
            phone,
            customer_key,
            auto_return,
            extra_data,
            fiscal_data,
            split_data,
        )
        for key in ("extra_data", "fiscal_data", "split_data"):
            if key in params:
                params[key] = json.dumps(params[key], separators=(",", ":"), ensure_ascii=False)
        return f"{self._host}/checkout?{urlencode(params)}"

    def build_form_fields(
        self,
        amount: int,
        transaction: str,
        description: str,
        success_url: str,
        fail_url: str,
        expires_at: int | None = None,
        phone: str | None = None,
        customer_key: str | None = None,
        auto_return: int | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> dict:
        params = self._params(
            amount,
            transaction,
            description,
            success_url,
            fail_url,
            expires_at,
            phone,
            customer_key,
            auto_return,
            extra_data,
            fiscal_data,
            split_data,
        )
        for key in ("extra_data", "fiscal_data", "split_data"):
            if key in params:
                params[key] = json.dumps(params[key], separators=(",", ":"), ensure_ascii=False)
        return params


class CheckoutResource(_CheckoutMixin, BaseResource):
    def create(
        self,
        amount: int,
        transaction: str,
        description: str,
        success_url: str,
        fail_url: str,
        expires_at: int | None = None,
        phone: str | None = None,
        customer_key: str | None = None,
        auto_return: int | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> str:
        body = self._params(
            amount,
            transaction,
            description,
            success_url,
            fail_url,
            expires_at,
            phone,
            customer_key,
            auto_return,
            extra_data,
            fiscal_data,
            split_data,
        )
        data = self._post("/checkout", body, {"Accept": "application/json"})
        return data["url"]


class AsyncCheckoutResource(_CheckoutMixin, AsyncBaseResource):
    async def create(
        self,
        amount: int,
        transaction: str,
        description: str,
        success_url: str,
        fail_url: str,
        expires_at: int | None = None,
        phone: str | None = None,
        customer_key: str | None = None,
        auto_return: int | None = None,
        extra_data: dict | None = None,
        fiscal_data: dict | None = None,
        split_data: list | None = None,
    ) -> str:
        body = self._params(
            amount,
            transaction,
            description,
            success_url,
            fail_url,
            expires_at,
            phone,
            customer_key,
            auto_return,
            extra_data,
            fiscal_data,
            split_data,
        )
        data = await self._post("/checkout", body, {"Accept": "application/json"})
        return data["url"]
