from __future__ import annotations

from dataclasses import dataclass, field

from sdk_payment_python.models.common import KvellModel


@dataclass
class PayoutDraft(KvellModel):
    id: int | None = None
    draft_guid: str | None = None
    payout_type: str | None = None
    status: str | None = None
    amount: int | None = None
    number: str | None = None
    recipient_full_name: str | None = None
    recipient_card_mask: str | None = None
    recipient_phone: str | None = None
    recipient_bank_id: str | None = None
    description: str | None = None
    comment: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    orders: list = field(default_factory=list)
    documents: list = field(default_factory=list)
