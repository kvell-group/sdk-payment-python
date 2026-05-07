from __future__ import annotations

from sdk_payment_python.models.certificate import CertificatePdf, CertificateTask
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class PayoutCertificateResource(BaseResource):
    def send_email(self, transaction: str, email: str) -> None:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, email]
        )
        self._post(f"/v1/orders/{transaction}/operation-certificate", {"email": email}, self._auth_headers(sig))

    def create_view(self, transaction: str) -> CertificateTask:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        return CertificateTask.from_dict(
            self._post(f"/v1/orders/{transaction}/operation-certificate/view", {}, self._auth_headers(sig))
        )

    def get_view(self, transaction: str, task_id: str) -> CertificateTask:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, task_id]
        )
        return CertificateTask.from_dict(
            self._get_params(
                f"/v1/orders/{transaction}/operation-certificate/view",
                {"task_id": task_id},
                self._auth_headers(sig),
            )
        )

    def pdf(self, transaction: str) -> CertificatePdf:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        return CertificatePdf.from_dict(
            self._get(f"/v1/orders/{transaction}/operation-certificate/pdf", self._auth_headers(sig))
        )


class AsyncPayoutCertificateResource(AsyncBaseResource):
    async def send_email(self, transaction: str, email: str) -> None:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, email]
        )
        await self._post(f"/v1/orders/{transaction}/operation-certificate", {"email": email}, self._auth_headers(sig))

    async def create_view(self, transaction: str) -> CertificateTask:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        return CertificateTask.from_dict(
            await self._post(f"/v1/orders/{transaction}/operation-certificate/view", {}, self._auth_headers(sig))
        )

    async def get_view(self, transaction: str, task_id: str) -> CertificateTask:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [transaction, task_id]
        )
        return CertificateTask.from_dict(
            await self._get_params(
                f"/v1/orders/{transaction}/operation-certificate/view",
                {"task_id": task_id},
                self._auth_headers(sig),
            )
        )

    async def pdf(self, transaction: str) -> CertificatePdf:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [transaction])
        return CertificatePdf.from_dict(
            await self._get(f"/v1/orders/{transaction}/operation-certificate/pdf", self._auth_headers(sig))
        )
