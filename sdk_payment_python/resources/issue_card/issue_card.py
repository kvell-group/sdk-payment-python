from __future__ import annotations

from sdk_payment_python.models.issue_card import IssueCardApplication, IssueCardDocs, IssueCardPayout, IssueCardResult
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class IssueCardResource(BaseResource):
    def __init__(self, settings, http, baas_host: str, payout_host: str):
        super().__init__(settings, http, baas_host)
        self._payout_host = payout_host.rstrip("/")

    def create(self, request_id: str, additional_data: dict) -> IssueCardApplication:
        body = {"request_id": request_id, "additional_data": additional_data}
        sig = KvellUtils.create_signature_by_json_body(
            self._settings.get_api_key(), self._settings.get_secret_key(), body
        )
        return IssueCardApplication.from_dict(self._post("/v1/issue-card/applications", body, self._auth_headers(sig)))

    def docs(self, application_id: str) -> IssueCardDocs:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [application_id]
        )
        return IssueCardDocs.from_dict(
            self._get(f"/v1/issue-card/applications/{application_id}/docs", self._auth_headers(sig))
        )

    def issue(self, application_id: str) -> IssueCardResult:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [application_id]
        )
        return IssueCardResult.from_dict(
            self._post(f"/v1/issue-card/applications/{application_id}/issue", {}, self._auth_headers(sig))
        )

    def payout(
        self,
        card_id: str,
        amount: int,
        transaction: str,
        description: str,
        fiscal_data: dict | None = None,
        extra_data: dict | None = None,
    ) -> IssueCardPayout:
        body: dict = {
            "card_id": card_id,
            "amount": amount,
            "transaction": transaction,
            "description": description,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        sig = KvellUtils.create_rsa_signature(self._settings.get_private_key(), body)
        headers = {"X-Api-Key": self._settings.get_api_key(), "X-Signature": sig}
        return IssueCardPayout.from_dict(
            self._handle_response(
                self._http.post(f"{self._payout_host}/v1/orders/payout/issue-card", json=body, headers=headers)
            )
        )


class AsyncIssueCardResource(AsyncBaseResource):
    def __init__(self, settings, http, baas_host: str, payout_host: str):
        super().__init__(settings, http, baas_host)
        self._payout_host = payout_host.rstrip("/")

    async def create(self, request_id: str, additional_data: dict) -> IssueCardApplication:
        body = {"request_id": request_id, "additional_data": additional_data}
        sig = KvellUtils.create_signature_by_json_body(
            self._settings.get_api_key(), self._settings.get_secret_key(), body
        )
        return IssueCardApplication.from_dict(
            await self._post("/v1/issue-card/applications", body, self._auth_headers(sig))
        )

    async def docs(self, application_id: str) -> IssueCardDocs:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [application_id]
        )
        return IssueCardDocs.from_dict(
            await self._get(f"/v1/issue-card/applications/{application_id}/docs", self._auth_headers(sig))
        )

    async def issue(self, application_id: str) -> IssueCardResult:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [application_id]
        )
        return IssueCardResult.from_dict(
            await self._post(f"/v1/issue-card/applications/{application_id}/issue", {}, self._auth_headers(sig))
        )

    async def payout(
        self,
        card_id: str,
        amount: int,
        transaction: str,
        description: str,
        fiscal_data: dict | None = None,
        extra_data: dict | None = None,
    ) -> IssueCardPayout:
        body: dict = {
            "card_id": card_id,
            "amount": amount,
            "transaction": transaction,
            "description": description,
        }
        if fiscal_data is not None:
            body["fiscal_data"] = fiscal_data
        if extra_data is not None:
            body["extra_data"] = extra_data
        sig = KvellUtils.create_rsa_signature(self._settings.get_private_key(), body)
        headers = {"X-Api-Key": self._settings.get_api_key(), "X-Signature": sig}
        return IssueCardPayout.from_dict(
            self._handle_response(
                await self._http.post(f"{self._payout_host}/v1/orders/payout/issue-card", json=body, headers=headers)
            )
        )
