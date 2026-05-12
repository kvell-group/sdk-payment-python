<p align="center">
  <img src="https://docs.kvell.group/img/logo.svg" alt="KVELL" width="200"/>
</p>

# KVELL Python SDK

![CI](https://github.com/kvell-group/sdk-payment-python/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Release](https://img.shields.io/github/v/release/kvell-group/sdk-payment-python?cacheSeconds=0)
![License](https://img.shields.io/badge/license-MIT-green)

Python SDK для [KVELL Payment API](https://docs.kvell.group/).

## Зависимости

- Python 3.9+
- `httpx`
- `pycryptodome` (RSA подписи для выплатных операций)

## Установка

```bash
pip install https://github.com/kvell-group/sdk-payment-python.git
```

## Быстрый старт

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

## Конфигурация

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

Все хост параметры по умолчанию настроены на продакшен окружение

---

## Ресурсы

### `client.payments.checkout` — Платежная страница

| Метод                                                                             | Возвращает | Описание                                                        |
|-----------------------------------------------------------------------------------|------------|-----------------------------------------------------------------|
| `build_url(amount, transaction, description, success_url, fail_url, ...)`         | `str`      | Получение ссылки на платежную страницу без регистрации операции |
| `build_form_fields(amount, transaction, description, success_url, fail_url, ...)` | `dict`     | Формирование списка полей для html формы                        |
| `create(amount, transaction, description, success_url, fail_url, ...)`            | `str`      | Получение ссылки на платежную страницу с регистрацией операции  |

Все три метода принимают одинаковый набор параметров:
`expires_at`, `phone`, `customer_key`, `auto_return`, `extra_data`, `fiscal_data`, `split_data`.

Сигнатура: `sha256(api_key + transaction + amount + secret_key)` (`expires_at` добавляется если передан).

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

### `client.payments.session` — Оплата через создание сессии (hosted fields / JS widget)

| Метод                                           | Возвращает       | Описание                         |
|-------------------------------------------------|------------------|----------------------------------|
| `create(amount, transaction, description, ...)` | `SessionCreated` | Создание сессии                  |
| `sbp(transaction, customer=None)`               | `SbpResult`      | Инициализация оплаты по СБП      |
| `sbp_b2b(transaction, customer=None)`           | `SbpResult`      | Инициализация оплаты по B2B СБП  |
| `alfapay(transaction, ip, customer=None)`       | `AlfaPayResult`  | Инициализация оплаты по Alfa Pay |

```python
session = client.payments.session.create(amount=5000, transaction="tx-2", description="Goods")
sbp = client.payments.session.sbp(transaction="tx-2")
print(sbp.form_url)  # redirect user here
```

---

### `client.payments.invoices` — Счета

| Метод                                              | Возвращает | Описание                                             |
|----------------------------------------------------|------------|------------------------------------------------------|
| `create(invoice_number, amount, description, ...)` | `Invoice`  | Создание счета                                       |
| `get(invoice_guid)`                                | `Invoice`  | Получение информации по счету по GUID идентификатору |
| `cancel(invoice_guid)`                             | `Invoice`  | Отмена счета                                         |

Опционально для `create`: `delivery_type`, `delivery_value`, `extra_data`, `fiscal_data`, `split_data`.

```python
invoice = client.payments.invoices.create(invoice_number="INV-001", amount=5000, description="Services")
print(invoice.url)     # send to customer
print(invoice.status)  # new | processing | canceled | completed | expired

client.payments.invoices.cancel(invoice.invoice_guid)
```

---

### `client.payments.transactions` — Транзакции

| Метод                                             | Возвращает          | Описание                                              |
|---------------------------------------------------|---------------------|-------------------------------------------------------|
| `get(transaction)`                                | `Transaction`       | Получение информации по транзакции по ID              |
| `list(page, size, status, date_from, date_to)`    | `list[Transaction]` | Список транзакций (BaaS хост)                         |
| `registry(email, transactions=None, orders=None)` | `None`              | Отправить PDF-реестр на email (BaaS хост)             |

`list()` отправляет заголовок `X-Request-Id` (UUID4); сигнатура: `sha256(api_key + request_id + secret_key)`.

```python
tx = client.payments.transactions.get("tx-123")
print(tx.status)  # new | processing | completed | refunded | part_refunded | ...

txs = client.payments.transactions.list(page=1, size=50, status="completed")

client.payments.transactions.registry("accountant@example.com", transactions=["tx-1", "tx-2"])
```

---

### `client.payments.refunds` — Возвраты платежей

| Метод                              | Возвращает    | Описание                                                  |
|------------------------------------|---------------|-----------------------------------------------------------|
| `create(transaction, amount=None)` | `Transaction` | Полный или частичный возврат по ID транзакции             |

Если `amount` не передан — выполняется полный возврат.

```python
# Полный возврат
refunded = client.payments.refunds.create("tx-123")

# Частичный возврат
partial = client.payments.refunds.create("tx-123", amount=1000)
```

---

### `client.payments.recurring` — Рекуррентные платежи

| Метод                                                                                          | Возвращает    | Описание                                        |
|------------------------------------------------------------------------------------------------|---------------|-------------------------------------------------|
| `rebill(parent_transaction, transaction, amount, description, ...)`                            | `Transaction` | Рекуррентный платёж по сохранённому инструменту |
| `rebill_from_profile(parent_transaction, transaction, amount, description, customer_key, ...)` | `Transaction` | Рекуррентный платёж из профиля покупателя       |

Опционально для обоих методов: `fiscal_data`, `extra_data`.

```python
new_tx = client.payments.recurring.rebill("tx-parent", "tx-new", 3000, "Подписка")

new_tx = client.payments.recurring.rebill_from_profile(
    "tx-parent", "tx-new", 3000, "Подписка", customer_key="cust-001"
)
```

---

### `client.payments.qr` — Статические QR-коды СБП

| Метод                                                     | Возвращает   | Описание                        |
|-----------------------------------------------------------|--------------|---------------------------------|
| `create(name, payment_purpose, qr_width, qr_height, ...)` | `QRTemplate` | Создание статичного QR-кода СБП |
| `get(qr_template_id)`                                     | `QRTemplate` | Получение статичного QR-кода    |

Опционально для `create`: `amount`, `start_date`, `end_date`.

```python
qr = client.payments.qr.create(name="Donation", payment_purpose="Charity", qr_width=300, qr_height=300)
print(qr.qr_image)    # PNG в base64
print(qr.qr_payload)  # сырые данные СБП
```

---

### `client.payouts.card` — Выплаты на карту (account2card)

Сигнатура: RSA/SHA256 (требуется `private_key` в настройках).

| Метод                                                           | Возвращает   | Описание                              |
|-----------------------------------------------------------------|--------------|---------------------------------------|
| `create(transaction, amount, description, account_number, ...)` | `PayoutCard` | Инициализация выплаты на карту        |
| `confirm(transaction, otp)`                                     | `PayoutCard` | Подтверждение выплаты с помощью OTP   |

Опционально для `create`: `customer_key`, `extra_data`, `fiscal_data`.

```python
payout = client.payouts.card.create(
    transaction="payout-1", amount=5000, description="Withdrawal",
    account_number="4111111111111111",
)
# payout.status == "pending_otp" → запросить OTP у пользователя

confirmed = client.payouts.card.confirm("payout-1", otp="123456")
```

---

### `client.payouts.sbp` — Выплаты через СБП

| Метод                                                                   | Возвращает       | Описание                                               |
|-------------------------------------------------------------------------|------------------|--------------------------------------------------------|
| `banks()`                                                               | `list[SbpBank]`  | Список банков-участников СБП                           |
| `phone_banks(phone)`                                                    | `list[SbpBank]`  | Банки, доступные для указанного номера телефона        |
| `check(phone, bank_id)`                                                 | `SbpCheck`       | Проверка получателя перед выплатой                     |
| `create(transaction, amount, description, phone, bank_id, ...)`         | `PayoutSbp`      | Инициализация выплаты через СБП (RSA/SHA256)           |
| `confirm(transaction, otp)`                                             | `PayoutSbp`      | Подтверждение выплаты через СБП с помощью OTP          |
| `check_status(request_id)`                                              | `SbpCheckStatus` | Получение статуса асинхронной проверки получателя      |

Опционально для `create`: `customer_key`, `extra_data`, `fiscal_data`.

```python
banks = client.payouts.sbp.banks()
phone_banks = client.payouts.sbp.phone_banks("+79001234567")

check = client.payouts.sbp.check("+79001234567", bank_id="bank-1")
print(check.fio)  # имя получателя

payout = client.payouts.sbp.create(
    transaction="sbp-1", amount=3000, description="Payout",
    phone="+79001234567", bank_id="bank-1",
)
confirmed = client.payouts.sbp.confirm("sbp-1", otp="654321")
```

---

### `client.payouts.drafts` — Черновики выплат

| Метод                                           | Возвращает    | Описание                          |
|-------------------------------------------------|---------------|-----------------------------------|
| `create(payout_type, amount, description, ...)` | `PayoutDraft` | Создание черновика выплаты        |
| `confirm(payout_draft_id)`                      | `PayoutDraft` | Подтверждение черновика по ID     |
| `confirm_by_number(number)`                     | `PayoutDraft` | Подтверждение черновика по номеру |
| `get(payout_draft_id)`                          | `PayoutDraft` | Получение черновика по ID         |
| `get_by_number(number)`                         | `PayoutDraft` | Получение черновика по номеру     |

Опционально для `create`: `number`, `recipient_bank_id`, `recipient_full_name`, `recipient_card_pan`, `recipient_card_token`, `recipient_phone`, `comment`.

```python
draft = client.payouts.drafts.create("sbp", 10000, "Salary", recipient_phone="+79001234567")
confirmed = client.payouts.drafts.confirm(draft.id)
```

---

### `client.payouts.limits` — Лимиты выплат

| Метод                                  | Возвращает    | Описание                    |
|----------------------------------------|---------------|-----------------------------|
| `list()`                               | `list[Limit]` | Список всех лимитов         |
| `create(amount, limit_type)`           | `Limit`       | Создание лимита             |
| `get(limit_id)`                        | `Limit`       | Получение лимита по ID      |
| `update(limit_id, amount, limit_type)` | `Limit`       | Обновление лимита           |
| `delete(limit_id)`                     | `None`        | Удаление лимита             |

```python
limit = client.payouts.limits.create(500000, "daily")
client.payouts.limits.delete(limit.id)
```

---

### `client.payouts.certificate` — Справки по выплатным операциям

| Метод                              | Возвращает        | Описание                                       |
|------------------------------------|-------------------|------------------------------------------------|
| `send_email(transaction, email)`   | `None`            | Отправить PDF-справку на email                 |
| `create_view(transaction)`         | `CertificateTask` | Запустить асинхронную генерацию справки        |
| `get_view(transaction, task_id)`   | `CertificateTask` | Получить статус генерации справки              |
| `pdf(transaction)`                 | `CertificatePdf`  | Получить прямую ссылку на PDF                  |

```python
task = client.payouts.certificate.create_view("tx-123")
# опрашиваем до task.status == "completed"
result = client.payouts.certificate.get_view("tx-123", task.task_id)
print(result.url)
```

---

### `client.payouts.nominal` — Номинальные счета

Сигнатура: RSA/SHA256 (требуется `private_key` в настройках).

| Метод                                                                                                                               | Возвращает      | Описание                                 |
|-------------------------------------------------------------------------------------------------------------------------------------|-----------------|------------------------------------------|
| `payout_by_requisites(transaction, amount, description, fio, inn, kvd, account, ...)` | `NominalPayout` | Выплата по банковским реквизитам         |
| `payout_sbp(transaction, amount, description, inn, kvd, phone, bank_bic, ...)`                                                      | `NominalPayout` | Выплата через СБП                        |

Опционально для `payout_by_requisites`: `snils`, `validate_self_employed`, `customer`, `tax`, `extra_data`, `fiscal_data`.

Опционально для `payout_sbp`: `fio`, `fio_check`, `validate_self_employed`, `customer`, `extra_data`, `fiscal_data`.

```python
payout = client.payouts.nominal.payout_by_requisites(
    transaction="tx-1", amount=100000, description="Выплата по договору №123",
    fio="Иванов Иван Иванович", inn="771234567890", kvd="1",
    account={
        "account_number": "40817810099910004312",
        "bank_bic": "044525225",
        "bank_cor_account": "30101810400000000225",
        "bank_name": "ПАО Сбербанк",
    },
)

payout = client.payouts.nominal.payout_sbp(
    transaction="tx-2", amount=50000, description="Выплата",
    inn="771234567890", kvd="1", phone="+79001234567", bank_bic="044525225",
    fio="Иванов Иван Иванович", fio_check=True,
)
```

---

### `client.payouts.balance` — Баланс счёта

| Метод                    | Возвращает | Описание                            |
|--------------------------|------------|-------------------------------------|
| `bank(account_id)`       | `Balance`  | Баланс банковского счёта            |
| `internal(account_id)`   | `Balance`  | Баланс внутреннего счёта            |

Сигнатура: `sha256(api_key + account_id + secret_key)`.

```python
balance = client.payouts.balance.bank("acc-123")
print(balance.amount, balance.hold, balance.available)
```

---

### `client.customers` — Профили покупателей и сохранённые карты

| Метод                                                                                               | Возвращает           | Описание                                                    |
|-----------------------------------------------------------------------------------------------------|----------------------|-------------------------------------------------------------|
| `create(customer_key, email, phone, name)`                                                          | `Customer`           | Создание покупателя                                         |
| `get(customer_key)`                                                                                 | `Customer`           | Получение покупателя                                        |
| `list(page, size)`                                                                                  | `list[Customer]`     | Список покупателей                                          |
| `update(customer_key, email, phone, name)`                                                          | `Customer`           | Обновление покупателя                                       |
| `cards_list(customer_key)`                                                                          | `list[CustomerCard]` | Список сохранённых карт                                     |
| `card_get(customer_key, card_id)`                                                                   | `CustomerCard`       | Получение сохранённой карты                                 |
| `card_delete(customer_key, card_id)`                                                                | `None`               | Удаление сохранённой карты                                  |
| `card_bind_url(customer_key)`                                                                       | `str`                | URL формы привязки карты (без HTTP-запроса)                 |
| `card_authorize_url(customer_key, transaction, amount, description, success_url, fail_url, ...)`    | `str`                | Привязка карты через реальное списание                      |
| `card_preauthorize_url(customer_key, transaction, amount, description, success_url, fail_url, ...)` | `str`                | Привязка карты через холд и отмену (без реального списания) |
| `card_payment(customer_key, card_token, transaction, amount, description, ...)`                     | `Transaction`        | Оплата сохранённой картой                                   |
| `card_payout(customer_key, card_token, transaction, amount, description)`                           | `Transaction`        | Выплата на сохранённую карту                                |

Опционально для `card_payment`: `fiscal_data`, `extra_data`. Опционально для `card_authorize_url` / `card_preauthorize_url`: `auto_return`.

Сигнатура для authorize/preauthorize: `sha256(api_key + customer_key + transaction + amount + success_url + fail_url + secret_key)`.

```python
customer = client.customers.create("cust-001", email="user@example.com")

# простая форма привязки карты
bind_url = client.customers.card_bind_url("cust-001")

# привязка через реальное списание
auth_url = client.customers.card_authorize_url(
    customer_key="cust-001", transaction="bind-tx-1", amount=0,
    description="Card binding", success_url="https://ok", fail_url="https://fail",
)

# привязка через холд и отмену
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

### `client.smz` — Самозанятые (СМЗ)

| Метод                                                                | Возвращает   | Описание                                  |
|----------------------------------------------------------------------|--------------|-------------------------------------------|
| `inn_check(inn)`                                                     | `InnCheck`   | Проверка статуса самозанятого по ИНН      |
| `create(inn, first_name, last_name, email, phone, second_name=None)` | `SmzClient`  | Регистрация клиента СМЗ                   |
| `receipt_create(inn, amount, service_name, description=None)`        | `SmzReceipt` | Создание чека о доходе                    |
| `receipt_get(receipt_id)`                                            | `SmzReceipt` | Получение чека по ID                      |
| `receipt_cancel(receipt_id)`                                         | `SmzReceipt` | Отмена чека                               |

```python
check = client.smz.inn_check("123456789012")
print(check.status)  # active / not_found / ...

smz_client = client.smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567")

receipt = client.smz.receipt_create("123456789012", amount=5000, service_name="Консультация")
print(receipt.status)
```

---

### `client.issue_card` — Выпуск карты

| Метод                                                    | Возвращает             | Описание                                            |
|----------------------------------------------------------|------------------------|-----------------------------------------------------|
| `create(request_id, additional_data)`                    | `IssueCardApplication` | Создание заявки на выпуск карты (BaaS хост)         |
| `docs(application_id)`                                   | `IssueCardDocs`        | Получение URL для подписания документов             |
| `issue(application_id)`                                  | `IssueCardResult`      | Выпуск карты после подписания документов            |
| `payout(card_id, amount, transaction, description, ...)` | `IssueCardPayout`      | Выплата на выпущенную карту (RSA/SHA256)            |

Опционально для `payout`: `fiscal_data`, `extra_data`.

```python
application = client.issue_card.create("req-001", {"first_name": "Иван", "last_name": "Иванов"})
docs = client.issue_card.docs(application.id)
print(docs.url)  # перенаправить пользователя для подписания

result = client.issue_card.issue(application.id)
print(result.card_mask)  # 411111******1111

payout = client.issue_card.payout(
    card_id=result.id, amount=10000, transaction="ic-payout-1", description="Salary"
)
```

---

## Колбэки

Проверка подписи входящих вебхуков KVELL:

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
    # обработка payload...
```

Алгоритм подписи: `sha256(api_key + raw_body + secret_key)`.

---

## Исключения

| Исключение             | Когда возникает                                                              |
|------------------------|------------------------------------------------------------------------------|
| `KvellError`           | Базовое исключение для всех ошибок SDK                                       |
| `KvellAPIError`        | HTTP 4xx/5xx ответ от API; содержит `.status_code` и `.body`                 |
| `KvellValidationError` | HTTP 422 ошибка валидации; содержит список `.errors`                         |

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

## Модели

Все объекты ответов — датаклассы с полной поддержкой автодополнения в IDE.

| Модель                 | Поля                                                                                               | Используется в                                                                              |
|------------------------|----------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| `SessionCreated`       | `ok`                                                                                               | `payments.session.create`                                                                   |
| `SbpResult`            | `form_url`                                                                                         | `payments.session.sbp`, `payments.session.sbp_b2b`                                          |
| `AlfaPayResult`        | `form_url`                                                                                         | `payments.session.alfapay`                                                                  |
| `Invoice`              | `invoice_guid`, `status`, `amount`, `url`, `created_at`, `expired_at`, ...                         | `payments.invoices.*`                                                                       |
| `Transaction`          | `id`, `transaction`, `status`, `amount`, `description`, `created_at`, ...                          | `payments.transactions.*`, `payments.refunds.*`, `payments.recurring.*`, `customers.card_*` |
| `QRTemplate`           | `id`, `name`, `payment_purpose`, `qr_payload`, `qr_image`, `currency`, ...                         | `payments.qr.*`                                                                             |
| `PayoutCard`           | `transaction`, `status`, `amount`, `id`, `description`, `created_at`, ...                          | `payouts.card.*`                                                                            |
| `PayoutSbp`            | `transaction`, `status`, `amount`, `id`, `description`, `created_at`, ...                          | `payouts.sbp.create`, `payouts.sbp.confirm`                                                 |
| `SbpBank`              | `id`, `name`, `bic`, `logo`                                                                        | `payouts.sbp.banks`, `payouts.sbp.phone_banks`                                              |
| `SbpCheck`             | `fio`, `bank_name`, `bank_bic`, `success`                                                          | `payouts.sbp.check`                                                                         |
| `Balance`              | `amount`, `hold`, `available`, `currency`, `account_id`                                            | `payouts.balance.*`                                                                         |
| `PayoutDraft`          | `id`, `draft_guid`, `payout_type`, `status`, `amount`, `number`, ...                               | `payouts.drafts.*`                                                                          |
| `Limit`                | `id`, `amount`, `type`                                                                             | `payouts.limits.*`                                                                          |
| `CertificateTask`      | `task_id`, `status`, `url`, `order_id`, `error_message`                                            | `payouts.certificate.create_view`, `.get_view`                                              |
| `CertificatePdf`       | `file_url`                                                                                         | `payouts.certificate.pdf`                                                                   |
| `SbpCheckStatus`       | `status`, `fio_nspk`, `nspk_id`, `error_message`, `recipient_account`                              | `payouts.sbp.check_status`                                                                  |
| `NominalPayout`        | `id`, `status`, `transaction`, `amount`, `commission`, `error_code`, `error_message`, `created_at` | `payouts.nominal.*`                                                                         |
| `Customer`             | `customer_key`, `id`, `email`, `phone`, `name`, `created_at`                                       | `customers.create/get/list/update`                                                          |
| `CustomerCard`         | `id`, `card_token`, `pan`, `brand`, `exp_month`, `exp_year`, `is_default`                          | `customers.cards_list`, `customers.card_get`                                                |
| `InnCheck`             | `status`, `message`                                                                                | `smz.inn_check`                                                                             |
| `SmzClient`            | `id`, `inn`, `first_name`, `last_name`, `email`, `phone`, ...                                      | `smz.create`                                                                                |
| `SmzReceipt`           | `id`, `inn`, `amount`, `service_name`, `status`, `remote_url`, ...                                 | `smz.receipt_*`                                                                             |
| `IssueCardApplication` | `id`, `status`, `request_id`, `remote_id`, `error_message`, `created`                              | `issue_card.create`                                                                         |
| `IssueCardDocs`        | `url`                                                                                              | `issue_card.docs`                                                                           |
| `IssueCardResult`      | `id`, `status`, `card_mask`, `card_expire`, `auth_code`, ...                                       | `issue_card.issue`                                                                          |
| `IssueCardPayout`      | `id`, `status`, `amount`, `commission`, `created_at`                                               | `issue_card.payout`                                                                         |
