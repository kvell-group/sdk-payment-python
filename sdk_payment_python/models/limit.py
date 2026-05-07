from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class Limit(KvellModel):
    id: int | None = None
    amount: int | None = None
    type: str | None = None
