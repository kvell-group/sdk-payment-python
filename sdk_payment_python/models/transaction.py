from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class Transaction(KvellModel):
    id: int
    status: str
    amount: int
    transaction: str
    description: str
    created_at: str
    commission: int | None = None
    refund_amount: int | None = None
    instrument: str | None = None
