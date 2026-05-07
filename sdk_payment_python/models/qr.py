from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class QRTemplate(KvellModel):
    id: str
    name: str
    payment_purpose: str
    qr_payload: str
    qr_image: str
    currency: str
    amount: int | None = None
    start_date: str | None = None
    end_date: str | None = None
