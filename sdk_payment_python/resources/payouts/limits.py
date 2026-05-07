from __future__ import annotations

from sdk_payment_python.models.limit import Limit
from sdk_payment_python.resources._base import AsyncBaseResource, BaseResource
from sdk_payment_python.utils import KvellUtils


class LimitsResource(BaseResource):
    def list(self) -> list[Limit]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [])
        data = self._get("/v1/points/limits", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [Limit.from_dict(item) for item in items]

    def create(self, amount: int, limit_type: str) -> Limit:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [amount, limit_type]
        )
        body = {"amount": amount, "type": limit_type}
        return Limit.from_dict(self._post("/v1/points/limits", body, self._auth_headers(sig)))

    def get(self, limit_id: int) -> Limit:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [limit_id])
        return Limit.from_dict(self._get(f"/v1/points/limits/{limit_id}", self._auth_headers(sig)))

    def update(self, limit_id: int, amount: int, limit_type: str) -> Limit:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [limit_id])
        body = {"amount": amount, "type": limit_type}
        return Limit.from_dict(self._patch_body(f"/v1/points/limits/{limit_id}", body, self._auth_headers(sig)))

    def delete(self, limit_id: int) -> None:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [limit_id])
        self._delete(f"/v1/points/limits/{limit_id}", self._auth_headers(sig))


class AsyncLimitsResource(AsyncBaseResource):
    async def list(self) -> list[Limit]:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [])
        data = await self._get("/v1/points/limits", self._auth_headers(sig))
        items = data if isinstance(data, list) else data.get("items", [])
        return [Limit.from_dict(item) for item in items]

    async def create(self, amount: int, limit_type: str) -> Limit:
        sig = KvellUtils.create_signature(
            self._settings.get_api_key(), self._settings.get_secret_key(), [amount, limit_type]
        )
        body = {"amount": amount, "type": limit_type}
        return Limit.from_dict(await self._post("/v1/points/limits", body, self._auth_headers(sig)))

    async def get(self, limit_id: int) -> Limit:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [limit_id])
        return Limit.from_dict(await self._get(f"/v1/points/limits/{limit_id}", self._auth_headers(sig)))

    async def update(self, limit_id: int, amount: int, limit_type: str) -> Limit:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [limit_id])
        body = {"amount": amount, "type": limit_type}
        return Limit.from_dict(await self._patch_body(f"/v1/points/limits/{limit_id}", body, self._auth_headers(sig)))

    async def delete(self, limit_id: int) -> None:
        sig = KvellUtils.create_signature(self._settings.get_api_key(), self._settings.get_secret_key(), [limit_id])
        await self._delete(f"/v1/points/limits/{limit_id}", self._auth_headers(sig))
