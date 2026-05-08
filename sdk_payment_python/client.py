from __future__ import annotations

import httpx

from sdk_payment_python.resources.customers.customers import AsyncCustomersResource, CustomersResource
from sdk_payment_python.resources.issue_card.issue_card import AsyncIssueCardResource, IssueCardResource
from sdk_payment_python.resources.payments.checkout import AsyncCheckoutResource, CheckoutResource
from sdk_payment_python.resources.payments.invoices import AsyncInvoicesResource, InvoicesResource
from sdk_payment_python.resources.payments.qr import AsyncQRResource, QRResource
from sdk_payment_python.resources.payments.recurring import AsyncRecurringResource, RecurringResource
from sdk_payment_python.resources.payments.refunds import AsyncRefundsResource, RefundsResource
from sdk_payment_python.resources.payments.session import AsyncSessionResource, SessionResource
from sdk_payment_python.resources.payments.transactions import AsyncTransactionsResource, TransactionsResource
from sdk_payment_python.resources.payouts.balance import AsyncBalanceResource, BalanceResource
from sdk_payment_python.resources.payouts.card import AsyncPayoutsCardResource, PayoutsCardResource
from sdk_payment_python.resources.payouts.certificate import AsyncPayoutCertificateResource, PayoutCertificateResource
from sdk_payment_python.resources.payouts.drafts import AsyncPayoutDraftsResource, PayoutDraftsResource
from sdk_payment_python.resources.payouts.limits import AsyncLimitsResource, LimitsResource
from sdk_payment_python.resources.payouts.nominal import AsyncNominalResource, NominalResource
from sdk_payment_python.resources.payouts.sbp import AsyncPayoutsSbpResource, PayoutsSbpResource
from sdk_payment_python.resources.smz.smz import AsyncSmzResource, SmzResource
from sdk_payment_python.settings import KvellSettings


class _Payments:
    checkout: CheckoutResource
    session: SessionResource
    invoices: InvoicesResource
    transactions: TransactionsResource
    refunds: RefundsResource
    recurring: RecurringResource
    qr: QRResource

    def __init__(self, settings: KvellSettings, http: httpx.Client):
        self.checkout = CheckoutResource(settings, http, settings.get_pay_host())
        self.session = SessionResource(settings, http, settings.get_api_host())
        self.invoices = InvoicesResource(settings, http, settings.get_api_host())
        self.transactions = TransactionsResource(settings, http, settings.get_api_host(), settings.get_baas_host())
        self.refunds = RefundsResource(settings, http, settings.get_api_host())
        self.recurring = RecurringResource(settings, http, settings.get_api_host())
        self.qr = QRResource(settings, http, settings.get_api_host())


class _Payouts:
    card: PayoutsCardResource
    sbp: PayoutsSbpResource
    balance: BalanceResource
    drafts: PayoutDraftsResource
    limits: LimitsResource
    certificate: PayoutCertificateResource
    nominal: NominalResource

    def __init__(self, settings: KvellSettings, http: httpx.Client):
        self.card = PayoutsCardResource(settings, http, settings.get_api_host())
        self.sbp = PayoutsSbpResource(settings, http, settings.get_api_host())
        self.balance = BalanceResource(settings, http, settings.get_api_host())
        self.drafts = PayoutDraftsResource(settings, http, settings.get_baas_host())
        self.limits = LimitsResource(settings, http, settings.get_baas_host())
        self.certificate = PayoutCertificateResource(settings, http, settings.get_api_host())
        self.nominal = NominalResource(settings, http, settings.get_api_host())


class _AsyncPayments:
    checkout: AsyncCheckoutResource
    session: AsyncSessionResource
    invoices: AsyncInvoicesResource
    transactions: AsyncTransactionsResource
    refunds: AsyncRefundsResource
    recurring: AsyncRecurringResource
    qr: AsyncQRResource

    def __init__(self, settings: KvellSettings, http: httpx.AsyncClient):
        self.checkout = AsyncCheckoutResource(settings, http, settings.get_pay_host())
        self.session = AsyncSessionResource(settings, http, settings.get_api_host())
        self.invoices = AsyncInvoicesResource(settings, http, settings.get_api_host())
        self.transactions = AsyncTransactionsResource(settings, http, settings.get_api_host(), settings.get_baas_host())
        self.refunds = AsyncRefundsResource(settings, http, settings.get_api_host())
        self.recurring = AsyncRecurringResource(settings, http, settings.get_api_host())
        self.qr = AsyncQRResource(settings, http, settings.get_api_host())


class _AsyncPayouts:
    card: AsyncPayoutsCardResource
    sbp: AsyncPayoutsSbpResource
    balance: AsyncBalanceResource
    drafts: AsyncPayoutDraftsResource
    limits: AsyncLimitsResource
    certificate: AsyncPayoutCertificateResource
    nominal: AsyncNominalResource

    def __init__(self, settings: KvellSettings, http: httpx.AsyncClient):
        self.card = AsyncPayoutsCardResource(settings, http, settings.get_api_host())
        self.sbp = AsyncPayoutsSbpResource(settings, http, settings.get_api_host())
        self.balance = AsyncBalanceResource(settings, http, settings.get_api_host())
        self.drafts = AsyncPayoutDraftsResource(settings, http, settings.get_baas_host())
        self.limits = AsyncLimitsResource(settings, http, settings.get_baas_host())
        self.certificate = AsyncPayoutCertificateResource(settings, http, settings.get_api_host())
        self.nominal = AsyncNominalResource(settings, http, settings.get_api_host())


class KvellPayment:
    payments: _Payments
    payouts: _Payouts
    customers: CustomersResource
    smz: SmzResource
    issue_card: IssueCardResource

    def __init__(self, settings: KvellSettings, timeout: float = 30.0):
        self._http = httpx.Client(timeout=timeout)
        self.payments = _Payments(settings, self._http)
        self.payouts = _Payouts(settings, self._http)
        self.customers = CustomersResource(settings, self._http, settings.get_api_host(), settings.get_customer_host())
        self.smz = SmzResource(settings, self._http, settings.get_baas_host())
        self.issue_card = IssueCardResource(settings, self._http, settings.get_baas_host(), settings.get_api_host())

    def close(self) -> None:
        self._http.close()

    def __enter__(self) -> KvellPayment:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()


class AsyncKvellPayment:
    payments: _AsyncPayments
    payouts: _AsyncPayouts
    customers: AsyncCustomersResource
    smz: AsyncSmzResource
    issue_card: AsyncIssueCardResource

    def __init__(self, settings: KvellSettings, timeout: float = 30.0):
        self._http = httpx.AsyncClient(timeout=timeout)
        self.payments = _AsyncPayments(settings, self._http)
        self.payouts = _AsyncPayouts(settings, self._http)
        self.customers = AsyncCustomersResource(
            settings, self._http, settings.get_api_host(), settings.get_customer_host()
        )
        self.smz = AsyncSmzResource(settings, self._http, settings.get_baas_host())
        self.issue_card = AsyncIssueCardResource(
            settings, self._http, settings.get_baas_host(), settings.get_api_host()
        )

    async def close(self) -> None:
        await self._http.aclose()

    async def __aenter__(self) -> AsyncKvellPayment:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()
