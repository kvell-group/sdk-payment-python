from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class IssueCardApplication(KvellModel):
    id: str | None = None
    status: str | None = None
    request_id: str | None = None
    remote_id: str | None = None
    error_message: str | None = None
    created: str | None = None


@dataclass
class IssueCardDocs(KvellModel):
    url: str | None = None


@dataclass
class IssueCardResult(KvellModel):
    id: str | None = None
    status: str | None = None
    remote_id: str | None = None
    auth_code: str | None = None
    response_code: str | None = None
    error_message: str | None = None
    card_mask: str | None = None
    card_expire: str | None = None
    created: str | None = None


@dataclass
class IssueCardPayout(KvellModel):
    id: int | None = None
    status: str | None = None
    amount: int | None = None
    commission: int | None = None
    created_at: str | None = None
