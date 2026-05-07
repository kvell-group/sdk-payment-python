from __future__ import annotations

from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class CertificateTask(KvellModel):
    task_id: str | None = None
    status: str | None = None
    url: str | None = None
    order_id: str | None = None
    error_message: str | None = None


@dataclass
class CertificatePdf(KvellModel):
    file_url: str | None = None
