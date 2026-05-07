from __future__ import annotations

from sdk_payment_python.models.balance import Balance
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class BalanceResource(BaseResource):
    def bank(self, account_id: str) -> Balance:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [account_id])
        return Balance.from_dict(self._get(f"/v1/balance/{account_id}/bank", self._auth_headers(sig)))

    def internal(self, account_id: str) -> Balance:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [account_id])
        return Balance.from_dict(self._get(f"/v1/balance/{account_id}", self._auth_headers(sig)))


class AsyncBalanceResource(AsyncBaseResource):
    async def bank(self, account_id: str) -> Balance:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [account_id])
        return Balance.from_dict(await self._get(f"/v1/balance/{account_id}/bank", self._auth_headers(sig)))

    async def internal(self, account_id: str) -> Balance:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [account_id])
        return Balance.from_dict(await self._get(f"/v1/balance/{account_id}", self._auth_headers(sig)))
