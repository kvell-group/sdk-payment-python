from __future__ import annotations

from sdk_payment_python.models.customer import Customer, CustomerCard
from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.settings import KvellSettings
from sdk_payment_python.utils import KvellUtils


class CustomersResource(BaseResource):
    def __init__(self, settings: KvellSettings, http, host: str, customer_host: str | None = None):
        super().__init__(settings, http, host)
        self._customer_host = (customer_host or host).rstrip("/")

    def create(
        self,
        customer_key: str,
        email: str | None = None,
        phone: str | None = None,
        name: str | None = None,
    ) -> Customer:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        body: dict = {"customer_key": customer_key}
        if email is not None:
            body["email"] = email
        if phone is not None:
            body["phone"] = phone
        if name is not None:
            body["name"] = name
        return Customer.from_dict(self._post("/v1/customers", body, self._auth_headers(sig)))

    def get(self, customer_key: str) -> Customer:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        return Customer.from_dict(self._get(f"/v1/customers/{customer_key}", self._auth_headers(sig)))

    def list(self, page: int = 1, size: int = 20) -> list[Customer]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [])
        data = self._get_params("/v1/customers", {"page": page, "size": size}, self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [Customer.from_dict(item) for item in items]

    def update(
        self,
        customer_key: str,
        email: str | None = None,
        phone: str | None = None,
        name: str | None = None,
    ) -> Customer:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        body: dict = {}
        if email is not None:
            body["email"] = email
        if phone is not None:
            body["phone"] = phone
        if name is not None:
            body["name"] = name
        return Customer.from_dict(self._patch_body(f"/v1/customers/{customer_key}", body, self._auth_headers(sig)))

    def cards_list(self, customer_key: str) -> list[CustomerCard]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        data = self._get(f"/v1/customers/{customer_key}/cards", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [CustomerCard.from_dict(item) for item in items]

    def card_get(self, customer_key: str, card_id: int) -> CustomerCard:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        return CustomerCard.from_dict(
            self._get(f"/v1/customers/{customer_key}/cards/{card_id}", self._auth_headers(sig))
        )

    def card_delete(self, customer_key: str, card_id: int) -> None:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        self._delete(f"/v1/customers/{customer_key}/cards/{card_id}", self._auth_headers(sig))

    def card_bind_url(self, customer_key: str) -> str:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        return f"{self._customer_host}/card-binding/{customer_key}/{sig}"

    def card_payment(
        self,
        customer_key: str,
        card_token: str,
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
            "customer_key": customer_key,
            "card_token": card_token,
            "transaction": transaction,
            "amount": amount,
            "description": description,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        return Transaction.from_dict(self._post("/v1/customers/cards/pay", body, self._auth_headers(sig)))

    def card_payout(
        self,
        customer_key: str,
        card_token: str,
        transaction: str,
        amount: int,
        description: str,
    ) -> Transaction:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body = {
            "customer_key": customer_key,
            "card_token": card_token,
            "transaction": transaction,
            "amount": amount,
            "description": description,
        }
        return Transaction.from_dict(self._post("/v1/customers/cards/payout", body, self._auth_headers(sig)))


class AsyncCustomersResource(AsyncBaseResource):
    def __init__(self, settings: KvellSettings, http, host: str, customer_host: str | None = None):
        super().__init__(settings, http, host)
        self._customer_host = (customer_host or host).rstrip("/")

    async def create(
        self,
        customer_key: str,
        email: str | None = None,
        phone: str | None = None,
        name: str | None = None,
    ) -> Customer:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        body: dict = {"customer_key": customer_key}
        if email is not None:
            body["email"] = email
        if phone is not None:
            body["phone"] = phone
        if name is not None:
            body["name"] = name
        return Customer.from_dict(await self._post("/v1/customers", body, self._auth_headers(sig)))

    async def get(self, customer_key: str) -> Customer:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        return Customer.from_dict(await self._get(f"/v1/customers/{customer_key}", self._auth_headers(sig)))

    async def list(self, page: int = 1, size: int = 20) -> list[Customer]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [])
        data = await self._get_params("/v1/customers", {"page": page, "size": size}, self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [Customer.from_dict(item) for item in items]

    async def update(
        self,
        customer_key: str,
        email: str | None = None,
        phone: str | None = None,
        name: str | None = None,
    ) -> Customer:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        body: dict = {}
        if email is not None:
            body["email"] = email
        if phone is not None:
            body["phone"] = phone
        if name is not None:
            body["name"] = name
        return Customer.from_dict(
            await self._patch_body(f"/v1/customers/{customer_key}", body, self._auth_headers(sig))
        )

    async def cards_list(self, customer_key: str) -> list[CustomerCard]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        data = await self._get(f"/v1/customers/{customer_key}/cards", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [CustomerCard.from_dict(item) for item in items]

    async def card_get(self, customer_key: str, card_id: int) -> CustomerCard:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        return CustomerCard.from_dict(
            await self._get(f"/v1/customers/{customer_key}/cards/{card_id}", self._auth_headers(sig))
        )

    async def card_delete(self, customer_key: str, card_id: int) -> None:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        await self._delete(f"/v1/customers/{customer_key}/cards/{card_id}", self._auth_headers(sig))

    def card_bind_url(self, customer_key: str) -> str:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [customer_key])
        return f"{self._customer_host}/card-binding/{customer_key}/{sig}"

    async def card_payment(
        self,
        customer_key: str,
        card_token: str,
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
            "customer_key": customer_key,
            "card_token": card_token,
            "transaction": transaction,
            "amount": amount,
            "description": description,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        return Transaction.from_dict(await self._post("/v1/customers/cards/pay", body, self._auth_headers(sig)))

    async def card_payout(
        self,
        customer_key: str,
        card_token: str,
        transaction: str,
        amount: int,
        description: str,
    ) -> Transaction:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, amount]
        )
        body = {
            "customer_key": customer_key,
            "card_token": card_token,
            "transaction": transaction,
            "amount": amount,
            "description": description,
        }
        return Transaction.from_dict(await self._post("/v1/customers/cards/payout", body, self._auth_headers(sig)))
