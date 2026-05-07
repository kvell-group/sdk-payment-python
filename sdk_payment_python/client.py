from __future__ import annotations

import httpx

from sdk_payment_python.resources.balance import AsyncBalanceResource, BalanceResource
from sdk_payment_python.resources.checkout import AsyncCheckoutResource, CheckoutResource
from sdk_payment_python.resources.customers import AsyncCustomersResource, CustomersResource
from sdk_payment_python.resources.invoices import AsyncInvoicesResource, InvoicesResource
from sdk_payment_python.resources.payouts import AsyncPayoutsResource, PayoutsResource
from sdk_payment_python.resources.qr import AsyncQRResource, QRResource
from sdk_payment_python.resources.session import AsyncSessionResource, SessionResource
from sdk_payment_python.resources.transactions import AsyncTransactionsResource, TransactionsResource
from sdk_payment_python.settings import KvellSettings


class KvellPayment:
    def __init__(self, settings: KvellSettings, timeout: float = 30.0):
        self._http = httpx.Client(timeout=timeout)
        self.checkout = CheckoutResource(settings, self._http, settings.get_payment_host())
        self.session = SessionResource(settings, self._http, settings.get_status_host())
        self.invoices = InvoicesResource(settings, self._http, settings.get_status_host())
        self.transactions = TransactionsResource(
            settings, self._http, settings.get_status_host(), settings.get_baas_host()
        )
        self.qr = QRResource(settings, self._http, settings.get_status_host())
        self.payouts = PayoutsResource(settings, self._http, settings.get_payout_host())
        self.balance = BalanceResource(settings, self._http, settings.get_balance_host())
        self.customers = CustomersResource(
            settings, self._http, settings.get_status_host(), settings.get_customer_host()
        )

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> KvellPayment:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncKvellPayment:
    def __init__(self, settings: KvellSettings, timeout: float = 30.0):
        self._http = httpx.AsyncClient(timeout=timeout)
        self.checkout = AsyncCheckoutResource(settings, self._http, settings.get_payment_host())
        self.session = AsyncSessionResource(settings, self._http, settings.get_status_host())
        self.invoices = AsyncInvoicesResource(settings, self._http, settings.get_status_host())
        self.transactions = AsyncTransactionsResource(
            settings, self._http, settings.get_status_host(), settings.get_baas_host()
        )
        self.qr = AsyncQRResource(settings, self._http, settings.get_status_host())
        self.payouts = AsyncPayoutsResource(settings, self._http, settings.get_payout_host())
        self.balance = AsyncBalanceResource(settings, self._http, settings.get_balance_host())
        self.customers = AsyncCustomersResource(
            settings, self._http, settings.get_status_host(), settings.get_customer_host()
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncKvellPayment:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
