from dataclasses import dataclass

from sdk_payment_python.models.common import KvellModel


@dataclass
class SessionCreated(KvellModel):
    ok: bool


@dataclass
class SbpResult(KvellModel):
    form_url: str


@dataclass
class AlfaPayResult(KvellModel):
    form_url: str
