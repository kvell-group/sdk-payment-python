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
    url = client.checkout.build_url(
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
    url = await client.checkout.create(...)
```

## Configuration

```python
from sdk_payment_python import KvellSettings

settings = KvellSettings(
    api_key="...",
    secret_key="...",
    private_key="-----BEGIN RSA PRIVATE KEY-----\n...",  # required for payouts
    payment_host="https://pay.kvell.group",              # checkout
    status_host="https://api.pay.kvell.group",           # payments, invoices, sessions
    payout_host="https://api.pay.kvell.group",           # payouts
    balance_host="https://api.pay.kvell.group",          # balance
    customer_host="https://customer.pay.kvell.group",    # card binding form
    baas_host="https://api.baas.kvell.group",            # transaction list
)
```

All host parameters have default values shown above.

---

## Resources

### `client.checkout` — Payment page

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
url = client.checkout.build_url(
    amount=10000, transaction="tx-1", description="Order",
    success_url="https://ok.example.com", fail_url="https://fail.example.com",
)

# HTML POST form
fields = client.checkout.build_form_fields(amount=10000, transaction="tx-1", ...)

# JSON API → returns URL
url = client.checkout.create(amount=10000, transaction="tx-1", ...)
```

---

### `client.session` — Payment session (hosted fields / JS widget)

| Method | Returns | Description |
|--------|---------|-------------|
| `create(amount, transaction, description, ...)` | `SessionCreated` | Create payment session |
| `sbp(transaction, customer=None)` | `SbpResult` | Initiate SBP payment |
| `sbp_b2b(transaction, customer=None)` | `SbpResult` | Initiate B2B SBP payment |
| `alfapay(transaction, ip, customer=None)` | `AlfaPayResult` | Initiate Alfa Pay payment |

```python
session = client.session.create(amount=5000, transaction="tx-2", description="Goods")
sbp = client.session.sbp(transaction="tx-2")
print(sbp.form_url)  # redirect user here
```

---

### `client.invoices` — Invoices

| Method | Returns | Description |
|--------|---------|-------------|
| `create(invoice_number, amount, description, ...)` | `Invoice` | Create invoice |
| `get(invoice_guid)` | `Invoice` | Get invoice by GUID |
| `cancel(invoice_guid)` | `Invoice` | Cancel invoice |

Optional for `create`: `delivery_type`, `delivery_value`, `extra_data`, `fiscal_data`, `split_data`.

```python
invoice = client.invoices.create(invoice_number="INV-001", amount=5000, description="Services")
print(invoice.url)     # send to customer
print(invoice.status)  # new | processing | canceled | completed | expired

client.invoices.cancel(invoice.invoice_guid)
```

---

### `client.transactions` — Transactions

| Method | Returns | Description |
|--------|---------|-------------|
| `get(transaction)` | `Transaction` | Get transaction by ID |
| `list(page, size, status, date_from, date_to)` | `list[Transaction]` | List transactions (BaaS host) |
| `refund(transaction, amount=None)` | `Transaction` | Full or partial refund |
| `rebill(parent_transaction, transaction, amount, description, ...)` | `Transaction` | Rebill from saved instrument |
| `rebill_from_profile(parent_transaction, transaction, amount, description, customer_key, ...)` | `Transaction` | Rebill from customer profile |

`list()` sends `X-Request-Id` (UUID4) header; signature: `sha256(api_key + request_id + secret_key)`.

Optional for `rebill` and `rebill_from_profile`: `fiscal_data`, `extra_data`.

```python
tx = client.transactions.get("tx-123")
print(tx.status)  # new | processing | completed | refunded | part_refunded | ...

txs = client.transactions.list(page=1, size=50, status="completed")

refunded = client.transactions.refund("tx-123")               # full refund
partial  = client.transactions.refund("tx-123", amount=1000)  # partial

new_tx = client.transactions.rebill("tx-parent", "tx-new", 3000, "Subscription")
```

---

### `client.payouts` — Payouts

#### Card payouts (`account2card`)

Signature: RSA/SHA256 (requires `private_key` in settings).

| Method | Returns | Description |
|--------|---------|-------------|
| `card_create(transaction, amount, description, account_number, ...)` | `PayoutCard` | Initiate card payout |
| `card_confirm(transaction, otp)` | `PayoutCard` | Confirm card payout with OTP |

Optional for `card_create`: `customer_key`, `extra_data`, `fiscal_data`.

```python
payout = client.payouts.card_create(
    transaction="payout-1", amount=5000, description="Withdrawal",
    account_number="4111111111111111",
)
# payout.status == "pending_otp" → ask user for OTP

confirmed = client.payouts.card_confirm("payout-1", otp="123456")
```

#### SBP payouts

| Method | Returns | Description |
|--------|---------|-------------|
| `sbp_banks()` | `list[SbpBank]` | List of SBP member banks |
| `sbp_phone_banks(phone)` | `list[SbpBank]` | Banks available for a phone number |
| `sbp_check(phone, bank_id)` | `SbpCheck` | Verify recipient before payout |
| `sbp_create(transaction, amount, description, phone, bank_id, ...)` | `PayoutSbp` | Initiate SBP payout (RSA/SHA256) |
| `sbp_confirm(transaction, otp)` | `PayoutSbp` | Confirm SBP payout with OTP |

Optional for `sbp_create`: `customer_key`, `extra_data`, `fiscal_data`.

```python
banks = client.payouts.sbp_banks()
phone_banks = client.payouts.sbp_phone_banks("+79001234567")

check = client.payouts.sbp_check("+79001234567", bank_id="bank-1")
print(check.fio)  # recipient name

payout = client.payouts.sbp_create(
    transaction="sbp-1", amount=3000, description="Payout",
    phone="+79001234567", bank_id="bank-1",
)
confirmed = client.payouts.sbp_confirm("sbp-1", otp="654321")
```

---

### `client.balance` — Account balance

| Method | Returns | Description |
|--------|---------|-------------|
| `bank(account_id)` | `Balance` | Bank account balance |
| `internal(account_id)` | `Balance` | Internal account balance |

Signature: `sha256(api_key + account_id + secret_key)`.

```python
balance = client.balance.bank("acc-123")
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
| `card_payment(customer_key, card_token, transaction, amount, description, ...)` | `Transaction` | Pay with saved card |
| `card_payout(customer_key, card_token, transaction, amount, description)` | `Transaction` | Payout to saved card |

Optional for `card_payment`: `fiscal_data`, `extra_data`.

```python
customer = client.customers.create("cust-001", email="user@example.com")

bind_url = client.customers.card_bind_url("cust-001")
# redirect customer to bind_url to save a card

cards = client.customers.cards_list("cust-001")
card = cards[0]

tx = client.customers.card_payment(
    customer_key="cust-001", card_token=card.card_token,
    transaction="tx-card", amount=2000, description="Order",
)
```

---

### `client.qr` — SBP QR templates

| Method | Returns | Description |
|--------|---------|-------------|
| `create(name, payment_purpose, qr_width, qr_height, ...)` | `QRTemplate` | Create SBP QR template |
| `get(qr_template_id)` | `QRTemplate` | Get QR template |

Optional for `create`: `amount`, `start_date`, `end_date`.

```python
qr = client.qr.create(name="Donation", payment_purpose="Charity", qr_width=300, qr_height=300)
print(qr.qr_image)    # base64-encoded PNG
print(qr.qr_payload)  # raw SBP payload
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
    invoice = client.invoices.create(invoice_number="INV-001", amount=5000, description="x")
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
| `SessionCreated` | `ok` | `session.create` |
| `SbpResult` | `form_url` | `session.sbp`, `session.sbp_b2b` |
| `AlfaPayResult` | `form_url` | `session.alfapay` |
| `Invoice` | `invoice_guid`, `status`, `amount`, `url`, `created_at`, `expired_at`, ... | `invoices.*` |
| `Transaction` | `id`, `transaction`, `status`, `amount`, `description`, `created_at`, ... | `transactions.*`, `customers.card_*` |
| `QRTemplate` | `id`, `name`, `payment_purpose`, `qr_payload`, `qr_image`, `currency`, ... | `qr.*` |
| `PayoutCard` | `transaction`, `status`, `amount`, `id`, `description`, `created_at`, ... | `payouts.card_*` |
| `PayoutSbp` | `transaction`, `status`, `amount`, `id`, `description`, `created_at`, ... | `payouts.sbp_create`, `payouts.sbp_confirm` |
| `SbpBank` | `id`, `name`, `bic`, `logo` | `payouts.sbp_banks`, `payouts.sbp_phone_banks` |
| `SbpCheck` | `fio`, `bank_name`, `bank_bic`, `success` | `payouts.sbp_check` |
| `Balance` | `amount`, `hold`, `available`, `currency`, `account_id` | `balance.*` |
| `Customer` | `customer_key`, `id`, `email`, `phone`, `name`, `created_at` | `customers.create/get/list/update` |
| `CustomerCard` | `id`, `card_token`, `pan`, `brand`, `exp_month`, `exp_year`, `is_default` | `customers.cards_list`, `customers.card_get` |
