from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class Balance(KvellModel):
    amount: int
    account_id: str | None = None
    currency: str | None = None
    hold: int | None = None
    available: int | None = None
