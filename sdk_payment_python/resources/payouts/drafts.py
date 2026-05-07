from __future__ import annotations

from sdk_payment_python.models.draft import PayoutDraft
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class PayoutDraftsResource(BaseResource):
    def create(
        self,
        payout_type: str,
        amount: int,
        description: str,
        number: str | None = None,
        recipient_bank_id: str | None = None,
        recipient_full_name: str | None = None,
        recipient_card_pan: str | None = None,
        recipient_card_token: str | None = None,
        recipient_phone: str | None = None,
        comment: str | None = None,
    ) -> PayoutDraft:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [amount])
        body: dict = {"payout_type": payout_type, "amount": amount, "description": description}
        if number is not None:
            body["number"] = number
        if recipient_bank_id is not None:
            body["recipient_bank_id"] = recipient_bank_id
        if recipient_full_name is not None:
            body["recipient_full_name"] = recipient_full_name
        if recipient_card_pan is not None:
            body["recipient_card_pan"] = recipient_card_pan
        if recipient_card_token is not None:
            body["recipient_card_token"] = recipient_card_token
        if recipient_phone is not None:
            body["recipient_phone"] = recipient_phone
        if comment is not None:
            body["comment"] = comment
        return PayoutDraft.from_dict(self._post("/v1/payout-drafts", body, self._auth_headers(sig)))

    def confirm(self, payout_draft_id: int) -> PayoutDraft:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [payout_draft_id]
        )
        return PayoutDraft.from_dict(
            self._post(f"/v1/payout-drafts/{payout_draft_id}/confirm", {}, self._auth_headers(sig))
        )

    def confirm_by_number(self, number: str) -> PayoutDraft:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [number])
        return PayoutDraft.from_dict(
            self._post(f"/v1/payout-drafts/number/{number}/confirm", {}, self._auth_headers(sig))
        )

    def get(self, payout_draft_id: int) -> PayoutDraft:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [payout_draft_id]
        )
        return PayoutDraft.from_dict(self._get(f"/v1/payout-drafts/{payout_draft_id}", self._auth_headers(sig)))

    def get_by_number(self, number: str) -> PayoutDraft:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [number])
        return PayoutDraft.from_dict(self._get(f"/v1/payout-drafts/number/{number}", self._auth_headers(sig)))


class AsyncPayoutDraftsResource(AsyncBaseResource):
    async def create(
        self,
        payout_type: str,
        amount: int,
        description: str,
        number: str | None = None,
        recipient_bank_id: str | None = None,
        recipient_full_name: str | None = None,
        recipient_card_pan: str | None = None,
        recipient_card_token: str | None = None,
        recipient_phone: str | None = None,
        comment: str | None = None,
    ) -> PayoutDraft:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [amount])
        body: dict = {"payout_type": payout_type, "amount": amount, "description": description}
        if number is not None:
            body["number"] = number
        if recipient_bank_id is not None:
            body["recipient_bank_id"] = recipient_bank_id
        if recipient_full_name is not None:
            body["recipient_full_name"] = recipient_full_name
        if recipient_card_pan is not None:
            body["recipient_card_pan"] = recipient_card_pan
        if recipient_card_token is not None:
            body["recipient_card_token"] = recipient_card_token
        if recipient_phone is not None:
            body["recipient_phone"] = recipient_phone
        if comment is not None:
            body["comment"] = comment
        return PayoutDraft.from_dict(await self._post("/v1/payout-drafts", body, self._auth_headers(sig)))

    async def confirm(self, payout_draft_id: int) -> PayoutDraft:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [payout_draft_id]
        )
        return PayoutDraft.from_dict(
            await self._post(f"/v1/payout-drafts/{payout_draft_id}/confirm", {}, self._auth_headers(sig))
        )

    async def confirm_by_number(self, number: str) -> PayoutDraft:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [number])
        return PayoutDraft.from_dict(
            await self._post(f"/v1/payout-drafts/number/{number}/confirm", {}, self._auth_headers(sig))
        )

    async def get(self, payout_draft_id: int) -> PayoutDraft:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [payout_draft_id]
        )
        return PayoutDraft.from_dict(await self._get(f"/v1/payout-drafts/{payout_draft_id}", self._auth_headers(sig)))

    async def get_by_number(self, number: str) -> PayoutDraft:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [number])
        return PayoutDraft.from_dict(await self._get(f"/v1/payout-drafts/number/{number}", self._auth_headers(sig)))
