# KVELL Payment Python SDK

Python SDK for the [KVELL Payment API](https://docs.kvell.group/).

## Requirements

- Python 3.9+
- `httpx`
- `pycryptodome` (RSA signatures for payouts)

## Installation

```bash
pip install kvell-sdk-payment-python
```

## Quick Start

```python
from sdk_payment_python import KvellPayment, KvellSettings

settings = KvellSettings(api_key="your_api_key", secret_key="your_secret_key")

with KvellPayment(settings) as client:
    url = client.payments.checkout.build_url(
        amount=10000,
        transaction="order-001",
        description="Order #001",
        success_url="https://example.com/success",
        fail_url="https://example.com/fail",
    )
```

### Async

```python
from sdk_payment_python import AsyncKvellPayment, KvellSettings

settings = KvellSettings(api_key="your_api_key", secret_key="your_secret_key")

async with AsyncKvellPayment(settings) as client:
    url = await client.payments.checkout.create(...)
```

## Configuration

```python
from sdk_payment_python import KvellSettings

settings = KvellSettings(
    api_key="...",
    secret_key="...",
    private_key="-----BEGIN RSA PRIVATE KEY-----\n...",  # required for payouts
    pay_host="https://pay.kvell.group",  # checkout
    api_host="https://api.pay.kvell.group",  # payments, payouts, invoices, sessions, balance
    customer_host="https://customer.pay.kvell.group",  # card binding form
    baas_host="https://api.baas.kvell.group",  # transaction list
)
```

All host parameters have default values shown above.

---

## Resources

### `client.payments.checkout` — Payment page

| Method | Returns | Description |
|--------|---------|-------------|
| `build_url(amount, transaction, description, success_url, fail_url, ...)` | `str` | GET-link to checkout page |
| `build_form_fields(amount, transaction, description, success_url, fail_url, ...)` | `dict` | Fields for HTML POST form |
| `create(amount, transaction, description, success_url, fail_url, ...)` | `str` | POST JSON → returns checkout URL |

All three methods accept the same optional parameters:
`expires_at`, `phone`, `customer_key`, `auto_return`, `extra_data`, `fiscal_data`, `split_data`.

Signature: `sha256(api_key + transaction + amount + secret_key)` (with `expires_at` appended if set).

```python
# GET redirect
url = client.payments.checkout.build_url(
    amount=10000, transaction="tx-1", description="Order",
    success_url="https://ok.example.com", fail_url="https://fail.example.com",
)

# HTML POST form
fields = client.payments.checkout.build_form_fields(amount=10000, transaction="tx-1", ...)

# JSON API → returns URL
url = client.payments.checkout.create(amount=10000, transaction="tx-1", ...)
```

---

### `client.payments.session` — Payment session (hosted fields / JS widget)

| Method | Returns | Description |
|--------|---------|-------------|
| `create(amount, transaction, description, ...)` | `SessionCreated` | Create payment session |
| `sbp(transaction, customer=None)` | `SbpResult` | Initiate SBP payment |
| `sbp_b2b(transaction, customer=None)` | `SbpResult` | Initiate B2B SBP payment |
| `alfapay(transaction, ip, customer=None)` | `AlfaPayResult` | Initiate Alfa Pay payment |

```python
session = client.payments.session.create(amount=5000, transaction="tx-2", description="Goods")
sbp = client.payments.session.sbp(transaction="tx-2")
print(sbp.form_url)  # redirect user here
```

---

### `client.payments.invoices` — Invoices

| Method | Returns | Description |
|--------|---------|-------------|
| `create(invoice_number, amount, description, ...)` | `Invoice` | Create invoice |
| `get(invoice_guid)` | `Invoice` | Get invoice by GUID |
| `cancel(invoice_guid)` | `Invoice` | Cancel invoice |

Optional for `create`: `delivery_type`, `delivery_value`, `extra_data`, `fiscal_data`, `split_data`.

```python
invoice = client.payments.invoices.create(invoice_number="INV-001", amount=5000, description="Services")
print(invoice.url)     # send to customer
print(invoice.status)  # new | processing | canceled | completed | expired

client.payments.invoices.cancel(invoice.invoice_guid)
```

---

### `client.payments.transactions` — Transactions

| Method | Returns | Description |
|--------|---------|-------------|
| `get(transaction)` | `Transaction` | Get transaction by ID |
| `list(page, size, status, date_from, date_to)` | `list[Transaction]` | List transactions (BaaS host) |
| `refund(transaction, amount=None)` | `Transaction` | Full or partial refund |
| `rebill(parent_transaction, transaction, amount, description, ...)` | `Transaction` | Rebill from saved instrument |
| `rebill_from_profile(parent_transaction, transaction, amount, description, customer_key, ...)` | `Transaction` | Rebill from customer profile |
| `registry(email, transactions=None, orders=None)` | `None` | Send PDF registry to email (BaaS host) |

`list()` sends `X-Request-Id` (UUID4) header; signature: `sha256(api_key + request_id + secret_key)`.

Optional for `rebill` and `rebill_from_profile`: `fiscal_data`, `extra_data`.

```python
tx = client.payments.transactions.get("tx-123")
print(tx.status)  # new | processing | completed | refunded | part_refunded | ...

txs = client.payments.transactions.list(page=1, size=50, status="completed")

refunded = client.payments.transactions.refund("tx-123")               # full refund
partial  = client.payments.transactions.refund("tx-123", amount=1000)  # partial

new_tx = client.payments.transactions.rebill("tx-parent", "tx-new", 3000, "Subscription")

client.payments.transactions.registry("accountant@example.com", transactions=["tx-1", "tx-2"])
```

---

### `client.payments.qr` — SBP QR templates

| Method | Returns | Description |
|--------|---------|-------------|
| `create(name, payment_purpose, qr_width, qr_height, ...)` | `QRTemplate` | Create SBP QR template |
| `get(qr_template_id)` | `QRTemplate` | Get QR template |

Optional for `create`: `amount`, `start_date`, `end_date`.

```python
qr = client.payments.qr.create(name="Donation", payment_purpose="Charity", qr_width=300, qr_height=300)
print(qr.qr_image)    # base64-encoded PNG
print(qr.qr_payload)  # raw SBP payload
```

---

### `client.payouts.card` — Card payouts (`account2card`)

Signature: RSA/SHA256 (requires `private_key` in settings).

| Method | Returns | Description |
|--------|---------|-------------|
| `create(transaction, amount, description, account_number, ...)` | `PayoutCard` | Initiate card payout |
| `confirm(transaction, otp)` | `PayoutCard` | Confirm card payout with OTP |

Optional for `create`: `customer_key`, `extra_data`, `fiscal_data`.

```python
payout = client.payouts.card.create(
    transaction="payout-1", amount=5000, description="Withdrawal",
    account_number="4111111111111111",
)
# payout.status == "pending_otp" → ask user for OTP

confirmed = client.payouts.card.confirm("payout-1", otp="123456")
```

---

### `client.payouts.sbp` — SBP payouts

| Method | Returns | Description |
|--------|---------|-------------|
| `banks()` | `list[SbpBank]` | List of SBP member banks |
| `phone_banks(phone)` | `list[SbpBank]` | Banks available for a phone number |
| `check(phone, bank_id)` | `SbpCheck` | Verify recipient before payout |
| `create(transaction, amount, description, phone, bank_id, ...)` | `PayoutSbp` | Initiate SBP payout (RSA/SHA256) |
| `confirm(transaction, otp)` | `PayoutSbp` | Confirm SBP payout with OTP |
| `check_status(request_id)` | `SbpCheckStatus` | Get status of async SBP recipient check |

Optional for `create`: `customer_key`, `extra_data`, `fiscal_data`.

```python
banks = client.payouts.sbp.banks()
phone_banks = client.payouts.sbp.phone_banks("+79001234567")

check = client.payouts.sbp.check("+79001234567", bank_id="bank-1")
print(check.fio)  # recipient name

payout = client.payouts.sbp.create(
    transaction="sbp-1", amount=3000, description="Payout",
    phone="+79001234567", bank_id="bank-1",
)
confirmed = client.payouts.sbp.confirm("sbp-1", otp="654321")
```

---

### `client.payouts.drafts` — Payout drafts

| Method | Returns | Description |
|--------|---------|-------------|
| `create(payout_type, amount, description, ...)` | `PayoutDraft` | Create payout draft |
| `confirm(payout_draft_id)` | `PayoutDraft` | Confirm draft by ID |
| `confirm_by_number(number)` | `PayoutDraft` | Confirm draft by number |
| `get(payout_draft_id)` | `PayoutDraft` | Get draft by ID |
| `get_by_number(number)` | `PayoutDraft` | Get draft by number |

Optional for `create`: `number`, `recipient_bank_id`, `recipient_full_name`, `recipient_card_pan`, `recipient_card_token`, `recipient_phone`, `comment`.

```python
draft = client.payouts.drafts.create("sbp", 10000, "Salary", recipient_phone="+79001234567")
confirmed = client.payouts.drafts.confirm(draft.id)
```

---

### `client.payouts.limits` — Payout limits

| Method | Returns | Description |
|--------|---------|-------------|
| `list()` | `list[Limit]` | List all limits |
| `create(amount, limit_type)` | `Limit` | Create limit |
| `get(limit_id)` | `Limit` | Get limit by ID |
| `update(limit_id, amount, limit_type)` | `Limit` | Update limit |
| `delete(limit_id)` | `None` | Delete limit |

```python
limit = client.payouts.limits.create(500000, "daily")
client.payouts.limits.delete(limit.id)
```

---

### `client.payouts.certificate` — Payout operation certificates

| Method | Returns | Description |
|--------|---------|-------------|
| `send_email(transaction, email)` | `None` | Send certificate PDF to email |
| `create_view(transaction)` | `CertificateTask` | Start async certificate generation |
| `get_view(transaction, task_id)` | `CertificateTask` | Poll generation status |
| `pdf(transaction)` | `CertificatePdf` | Get direct PDF link |

```python
task = client.payouts.certificate.create_view("tx-123")
# poll until task.status == "completed"
result = client.payouts.certificate.get_view("tx-123", task.task_id)
print(result.url)
```

---

### `client.payouts.balance` — Account balance

| Method | Returns | Description |
|--------|---------|-------------|
| `bank(account_id)` | `Balance` | Bank account balance |
| `internal(account_id)` | `Balance` | Internal account balance |

Signature: `sha256(api_key + account_id + secret_key)`.

```python
balance = client.payouts.balance.bank("acc-123")
print(balance.amount, balance.hold, balance.available)
```

---

### `client.customers` — Customer profiles & saved cards

| Method | Returns | Description |
|--------|---------|-------------|
| `create(customer_key, email, phone, name)` | `Customer` | Create customer |
| `get(customer_key)` | `Customer` | Get customer |
| `list(page, size)` | `list[Customer]` | List customers |
| `update(customer_key, email, phone, name)` | `Customer` | Update customer |
| `cards_list(customer_key)` | `list[CustomerCard]` | List saved cards |
| `card_get(customer_key, card_id)` | `CustomerCard` | Get saved card |
| `card_delete(customer_key, card_id)` | `None` | Delete saved card |
| `card_bind_url(customer_key)` | `str` | URL for card binding form (no HTTP request) |
| `card_authorize_url(customer_key, transaction, amount, description, success_url, fail_url, ...)` | `str` | Card binding via real authorization charge |
| `card_preauthorize_url(customer_key, transaction, amount, description, success_url, fail_url, ...)` | `str` | Card binding via hold + cancel (no real charge) |
| `card_payment(customer_key, card_token, transaction, amount, description, ...)` | `Transaction` | Pay with saved card |
| `card_payout(customer_key, card_token, transaction, amount, description)` | `Transaction` | Payout to saved card |

Optional for `card_payment`: `fiscal_data`, `extra_data`. Optional for `card_authorize_url` / `card_preauthorize_url`: `auto_return`.

Signature for authorize/preauthorize: `sha256(api_key + customer_key + transaction + amount + success_url + fail_url + secret_key)`.

```python
customer = client.customers.create("cust-001", email="user@example.com")

# simple card binding form
bind_url = client.customers.card_bind_url("cust-001")

# binding with authorization (real or zero-amount charge)
auth_url = client.customers.card_authorize_url(
    customer_key="cust-001", transaction="bind-tx-1", amount=0,
    description="Card binding", success_url="https://ok", fail_url="https://fail",
)

# binding with hold + cancel (funds briefly frozen)
preauth_url = client.customers.card_preauthorize_url(
    customer_key="cust-001", transaction="bind-tx-2", amount=100,
    description="Card binding", success_url="https://ok", fail_url="https://fail",
)

cards = client.customers.cards_list("cust-001")
card = cards[0]

tx = client.customers.card_payment(
    customer_key="cust-001", card_token=card.card_token,
    transaction="tx-card", amount=2000, description="Order",
)
```

---

### `client.smz` — Self-employed (SMZ / самозанятые)

| Method | Returns | Description |
|--------|---------|-------------|
| `inn_check(inn)` | `InnCheck` | Check self-employed status by INN |
| `create(inn, first_name, last_name, email, phone, second_name=None)` | `SmzClient` | Register SMZ client |
| `receipt_create(inn, amount, service_name, description=None)` | `SmzReceipt` | Create income receipt |
| `receipt_get(receipt_id)` | `SmzReceipt` | Get receipt by ID |
| `receipt_cancel(receipt_id)` | `SmzReceipt` | Cancel receipt |

```python
check = client.smz.inn_check("123456789012")
print(check.status)  # active / not_found / ...

smz_client = client.smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567")

receipt = client.smz.receipt_create("123456789012", amount=5000, service_name="Консультация")
print(receipt.status)
```

---

### `client.issue_card` — Issue card

| Method | Returns | Description |
|--------|---------|-------------|
| `create(request_id, additional_data)` | `IssueCardApplication` | Create card issue application (BaaS host) |
| `docs(application_id)` | `IssueCardDocs` | Get documents signing URL |
| `issue(application_id)` | `IssueCardResult` | Issue card after documents signed |
| `payout(card_id, amount, transaction, description, ...)` | `IssueCardPayout` | Payout to issued card (RSA/SHA256) |

Optional for `payout`: `fiscal_data`, `extra_data`.

```python
application = client.issue_card.create("req-001", {"first_name": "Иван", "last_name": "Иванов"})
docs = client.issue_card.docs(application.id)
print(docs.url)  # redirect user to sign documents

result = client.issue_card.issue(application.id)
print(result.card_mask)  # 411111******1111

payout = client.issue_card.payout(
    card_id=result.id, amount=10000, transaction="ic-payout-1", description="Salary"
)
```

---

## Callbacks

Verify the signature of incoming KVELL webhook callbacks:

```python
from sdk_payment_python.utils import KvellUtils

def handle_webhook(request):
    signature = request.headers.get("X-Signature")
    is_valid = KvellUtils.verify_callback_signature(
        api_key=settings.get_api_key(),
        raw_body=request.body.decode(),
        secret_key=settings.get_secret_key(),
        signature=signature,
    )
    if not is_valid:
        return 403
    # process payload...
```

Signature algorithm: `sha256(api_key + raw_body + secret_key)`.

---

## Exceptions

| Exception | When |
|-----------|------|
| `KvellError` | Base exception for all SDK errors |
| `KvellAPIError` | HTTP 4xx/5xx response from the API; has `.status_code` and `.body` |
| `KvellValidationError` | HTTP 422 validation error; has `.errors` list |

```python
from sdk_payment_python import KvellAPIError, KvellValidationError

try:
    invoice = client.payments.invoices.create(invoice_number="INV-001", amount=5000, description="x")
except KvellValidationError as e:
    print(e.errors)        # [{"message": "...", "code": 2}]
except KvellAPIError as e:
    print(e.status_code, e.body)
```

---

## Models

All response objects are dataclasses with full IDE autocomplete.

| Model | Fields | Used in |
|-------|--------|---------|
| `SessionCreated` | `ok` | `payments.session.create` |
| `SbpResult` | `form_url` | `payments.session.sbp`, `payments.session.sbp_b2b` |
| `AlfaPayResult` | `form_url` | `payments.session.alfapay` |
| `Invoice` | `invoice_guid`, `status`, `amount`, `url`, `created_at`, `expired_at`, ... | `payments.invoices.*` |
| `Transaction` | `id`, `transaction`, `status`, `amount`, `description`, `created_at`, ... | `payments.transactions.*`, `customers.card_*` |
| `QRTemplate` | `id`, `name`, `payment_purpose`, `qr_payload`, `qr_image`, `currency`, ... | `payments.qr.*` |
| `PayoutCard` | `transaction`, `status`, `amount`, `id`, `description`, `created_at`, ... | `payouts.card.*` |
| `PayoutSbp` | `transaction`, `status`, `amount`, `id`, `description`, `created_at`, ... | `payouts.sbp.create`, `payouts.sbp.confirm` |
| `SbpBank` | `id`, `name`, `bic`, `logo` | `payouts.sbp.banks`, `payouts.sbp.phone_banks` |
| `SbpCheck` | `fio`, `bank_name`, `bank_bic`, `success` | `payouts.sbp.check` |
| `Balance` | `amount`, `hold`, `available`, `currency`, `account_id` | `payouts.balance.*` |
| `PayoutDraft` | `id`, `draft_guid`, `payout_type`, `status`, `amount`, `number`, ... | `payouts.drafts.*` |
| `Limit` | `id`, `amount`, `type` | `payouts.limits.*` |
| `CertificateTask` | `task_id`, `status`, `url`, `order_id`, `error_message` | `payouts.certificate.create_view`, `.get_view` |
| `CertificatePdf` | `file_url` | `payouts.certificate.pdf` |
| `SbpCheckStatus` | `status`, `fio_nspk`, `nspk_id`, `error_message`, `recipient_account` | `payouts.sbp.check_status` |
| `Customer` | `customer_key`, `id`, `email`, `phone`, `name`, `created_at` | `customers.create/get/list/update` |
| `CustomerCard` | `id`, `card_token`, `pan`, `brand`, `exp_month`, `exp_year`, `is_default` | `customers.cards_list`, `customers.card_get` |
| `InnCheck` | `status`, `message` | `smz.inn_check` |
| `SmzClient` | `id`, `inn`, `first_name`, `last_name`, `email`, `phone`, ... | `smz.create` |
| `SmzReceipt` | `id`, `inn`, `amount`, `service_name`, `status`, `remote_url`, ... | `smz.receipt_*` |
| `IssueCardApplication` | `id`, `status`, `request_id`, `remote_id`, `error_message`, `created` | `issue_card.create` |
| `IssueCardDocs` | `url` | `issue_card.docs` |
| `IssueCardResult` | `id`, `status`, `card_mask`, `card_expire`, `auth_code`, ... | `issue_card.issue` |
| `IssueCardPayout` | `id`, `status`, `amount`, `commission`, `created_at` | `issue_card.payout` |
