from __future__ import annotations

import pytest

from sdk_payment_python.models.limit import Limit
from sdk_payment_python.resources.payouts.limits import LimitsResource
from tests.conftest import BASE_HOST, make_response

LIMIT_DATA = {"id": 1, "amount": 500000, "type": "daily"}


@pytest.fixture
def limits(settings, mock_http):
    return LimitsResource(settings, mock_http, BASE_HOST)


class TestLimitsList:
    def test_returns_list_of_limits(self, limits, mock_http):
        mock_http.get.return_value = make_response(200, [LIMIT_DATA])
        result = limits.list()
        assert len(result) == 1
        assert isinstance(result[0], Limit)

    def test_gets_correct_path(self, limits, mock_http):
        mock_http.get.return_value = make_response(200, [])
        limits.list()
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/points/limits"

    def test_returns_from_items_key(self, limits, mock_http):
        mock_http.get.return_value = make_response(200, {"items": [LIMIT_DATA, LIMIT_DATA]})
        result = limits.list()
        assert len(result) == 2


class TestLimitsCreate:
    def test_returns_limit(self, limits, mock_http):
        mock_http.post.return_value = make_response(200, LIMIT_DATA)
        result = limits.create(500000, "daily")
        assert isinstance(result, Limit)
        assert result.amount == 500000

    def test_posts_to_correct_path(self, limits, mock_http):
        mock_http.post.return_value = make_response(200, LIMIT_DATA)
        limits.create(500000, "daily")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/points/limits"

    def test_body_contains_amount_and_type(self, limits, mock_http):
        mock_http.post.return_value = make_response(200, LIMIT_DATA)
        limits.create(500000, "daily")
        body = mock_http.post.call_args[1]["json"]
        assert body["amount"] == 500000
        assert body["type"] == "daily"


class TestLimitsGet:
    def test_returns_limit(self, limits, mock_http):
        mock_http.get.return_value = make_response(200, LIMIT_DATA)
        result = limits.get(1)
        assert isinstance(result, Limit)
        assert result.id == 1

    def test_gets_correct_path(self, limits, mock_http):
        mock_http.get.return_value = make_response(200, LIMIT_DATA)
        limits.get(1)
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/points/limits/1"


class TestLimitsUpdate:
    def test_returns_limit(self, limits, mock_http):
        mock_http.patch.return_value = make_response(200, {**LIMIT_DATA, "amount": 600000})
        result = limits.update(1, 600000, "daily")
        assert isinstance(result, Limit)
        assert result.amount == 600000

    def test_patches_correct_path(self, limits, mock_http):
        mock_http.patch.return_value = make_response(200, LIMIT_DATA)
        limits.update(1, 600000, "daily")
        assert mock_http.patch.call_args[0][0] == f"{BASE_HOST}/v1/points/limits/1"

    def test_body_has_amount_and_type(self, limits, mock_http):
        mock_http.patch.return_value = make_response(200, LIMIT_DATA)
        limits.update(1, 600000, "monthly")
        body = mock_http.patch.call_args[1]["json"]
        assert body["amount"] == 600000
        assert body["type"] == "monthly"


class TestLimitsDelete:
    def test_deletes_correct_path(self, limits, mock_http):
        mock_http.delete.return_value = make_response(200, {})
        limits.delete(1)
        assert mock_http.delete.call_args[0][0] == f"{BASE_HOST}/v1/points/limits/1"

    def test_uses_sha256_signature(self, limits, mock_http):
        mock_http.delete.return_value = make_response(200, {})
        limits.delete(1)
        headers = mock_http.delete.call_args[1]["headers"]
        assert "X-Signature" in headers
