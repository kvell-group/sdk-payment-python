from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class Customer(KvellModel):
    customer_key: str
    id: int | None = None
    email: str | None = None
    phone: str | None = None
    name: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


@dataclass
class CustomerCard(KvellModel):
    id: int | None = None
    card_token: str | None = None
    pan: str | None = None
    exp_month: str | None = None
    exp_year: str | None = None
    brand: str | None = None
    created_at: str | None = None
    is_default: bool | None = None
