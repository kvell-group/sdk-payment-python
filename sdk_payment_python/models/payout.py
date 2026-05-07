from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class PayoutCard(KvellModel):
    transaction: str
    status: str
    amount: int
    id: int | None = None
    description: str | None = None
    created_at: str | None = None
    commission: int | None = None
    instrument: str | None = None


@dataclass
class PayoutSbp(KvellModel):
    transaction: str
    status: str
    amount: int
    id: int | None = None
    description: str | None = None
    created_at: str | None = None
    commission: int | None = None
    instrument: str | None = None


@dataclass
class SbpBank(KvellModel):
    id: str
    name: str
    bic: str | None = None
    logo: str | None = None


@dataclass
class SbpCheck(KvellModel):
    fio: str | None = None
    bank_name: str | None = None
    bank_bic: str | None = None
    success: bool | None = None
    phone: str | None = None
    bank_id: str | None = None


@dataclass
class SbpCheckStatus(KvellModel):
    status: str | None = None
    fio_nspk: str | None = None
    nspk_id: str | None = None
    error_message: str | None = None
    recipient_account: str | None = None
