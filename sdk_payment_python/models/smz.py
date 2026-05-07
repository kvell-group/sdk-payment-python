from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class InnCheck(KvellModel):
    status: str | None = None
    message: str | None = None


@dataclass
class SmzClient(KvellModel):
    id: int | None = None
    inn: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    second_name: str | None = None
    email: str | None = None
    phone: str | None = None
    created_at: str | None = None


@dataclass
class SmzReceipt(KvellModel):
    id: int | None = None
    inn: str | None = None
    amount: int | None = None
    service_name: str | None = None
    description: str | None = None
    status: str | None = None
    remote_url: str | None = None
    error_message: str | None = None
    created_at: str | None = None
