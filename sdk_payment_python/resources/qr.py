from __future__ import annotations

from sdk_payment_python.models.qr import QRTemplate
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class QRResource(BaseResource):
    def create(
        self,
        name: str,
        payment_purpose: str,
        qr_width: int,
        qr_height: int,
        amount: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> QRTemplate:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [name])
        body: dict = {
            "name": name,
            "payment_purpose": payment_purpose,
            "qr_width": qr_width,
            "qr_height": qr_height,
        }
        if amount is not None:
            body["amount"] = amount
        if start_date is not None:
            body["start_date"] = start_date
        if end_date is not None:
            body["end_date"] = end_date
        return QRTemplate.from_dict(self._post("/v1/qr-templates/sbp", body, self._auth_headers(sig)))

    def get(self, qr_template_id: str) -> QRTemplate:
        return QRTemplate.from_dict(self._get(f"/v1/qr-templates/{qr_template_id}", self._key_headers()))


class AsyncQRResource(AsyncBaseResource):
    async def create(
        self,
        name: str,
        payment_purpose: str,
        qr_width: int,
        qr_height: int,
        amount: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> QRTemplate:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [name])
        body: dict = {
            "name": name,
            "payment_purpose": payment_purpose,
            "qr_width": qr_width,
            "qr_height": qr_height,
        }
        if amount is not None:
            body["amount"] = amount
        if start_date is not None:
            body["start_date"] = start_date
        if end_date is not None:
            body["end_date"] = end_date
        return QRTemplate.from_dict(await self._post("/v1/qr-templates/sbp", body, self._auth_headers(sig)))

    async def get(self, qr_template_id: str) -> QRTemplate:
        return QRTemplate.from_dict(await self._get(f"/v1/qr-templates/{qr_template_id}", self._key_headers()))
