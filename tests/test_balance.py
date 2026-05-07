from __future__ import annotations

import pytest

from sdk_payment_python.models.balance import Balance
from sdk_payment_python.resources.payouts.balance import BalanceResource
from tests.conftest import BASE_HOST, make_response

BALANCE_DATA = {"amount": 100000, "currency": "RUB", "hold": 5000, "available": 95000}


@pytest.fixture
def balance(settings, mock_http):
    return BalanceResource(settings, mock_http, BASE_HOST)


class TestBalanceBank:
    def test_returns_balance(self, balance, mock_http):
        mock_http.get.return_value = make_response(200, BALANCE_DATA)
        result = balance.bank("acc-123")
        assert isinstance(result, Balance)
        assert result.amount == 100000

    def test_gets_correct_path(self, balance, mock_http):
        mock_http.get.return_value = make_response(200, BALANCE_DATA)
        balance.bank("acc-123")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/balance/acc-123/bank"

    def test_uses_auth_headers(self, balance, mock_http):
        mock_http.get.return_value = make_response(200, BALANCE_DATA)
        balance.bank("acc-123")
        headers = mock_http.get.call_args[1]["headers"]
        assert "X-Api-Key" in headers
        assert "X-Signature" in headers


class TestBalanceInternal:
    def test_returns_balance(self, balance, mock_http):
        mock_http.get.return_value = make_response(200, BALANCE_DATA)
        result = balance.internal("acc-123")
        assert isinstance(result, Balance)

    def test_gets_correct_path(self, balance, mock_http):
        mock_http.get.return_value = make_response(200, BALANCE_DATA)
        balance.internal("acc-123")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/balance/acc-123"
