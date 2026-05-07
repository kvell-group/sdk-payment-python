from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class Invoice(KvellModel):
    invoice_guid: str
    status: str
    amount: int
    url: str
    created_at: str
    expired_at: str
    id: int | None = None
    invoice_number: str | None = None
    description: str | None = None
    delivery_type: str | None = None
    delivery_value: str | None = None
