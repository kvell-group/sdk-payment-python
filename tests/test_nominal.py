from __future__ import annotations

from unittest.mock import patch

import pytest

from sdk_payment_python.models.payout import NominalPayout
from sdk_payment_python.resources.payouts.nominal import NominalResource
from tests.conftest import BASE_HOST, make_response

NOMINAL_DATA = {
    "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "status": "processing",
    "transaction": "tx-nominal-1",
    "amount": 100000,
    "commission": 0,
    "description": "Выплата по договору",
    "additional_data": None,
    "error_code": None,
    "error_message": None,
    "created_at": "2024-01-15T10:30:00",
}

ACCOUNT = {
    "account_number": "40817810099910004312",
    "bank_bic": "044525225",
    "bank_cor_account": "30101810400000000225",
    "bank_name": "ПАО Сбербанк",
}


@pytest.fixture
def nominal(settings, mock_http):
    return NominalResource(settings, mock_http, BASE_HOST)


class TestNominalPayoutByRequisites:
    def _call(self, nominal, mock_http, **kwargs):
        mock_http.post.return_value = make_response(200, NOMINAL_DATA)
        with patch.object(nominal, "_rsa_headers", return_value={"X-Api-Key": "key", "X-Signature": "sig"}):
            return nominal.payout_by_requisites(
                transaction="tx-nominal-1",
                amount=100000,
                description="Выплата по договору",
                fio="Иванов Иван Иванович",
                inn="771234567890",
                kvd="1",
                account_number=ACCOUNT["account_number"],
                bank_bic=ACCOUNT["bank_bic"],
                bank_cor_account=ACCOUNT["bank_cor_account"],
                bank_name=ACCOUNT["bank_name"],
                **kwargs,
            )

    def test_returns_nominal_payout(self, nominal, mock_http):
        result = self._call(nominal, mock_http)
        assert isinstance(result, NominalPayout)
        assert result.transaction == "tx-nominal-1"
        assert result.status == "processing"

    def test_posts_to_correct_path(self, nominal, mock_http):
        self._call(nominal, mock_http)
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/payout/smartcontract/fl/sber"

    def test_body_contains_required_fields(self, nominal, mock_http):
        self._call(nominal, mock_http)
        body = mock_http.post.call_args[1]["json"]
        assert body["transaction"] == "tx-nominal-1"
        assert body["inn"] == "771234567890"
        assert body["kvd"] == "1"
        assert body["account"]["bank_bic"] == ACCOUNT["bank_bic"]

    def test_optional_snils_sent(self, nominal, mock_http):
        self._call(nominal, mock_http, snils="123-456-789 01")
        body = mock_http.post.call_args[1]["json"]
        assert body["snils"] == "123-456-789 01"

    def test_optional_fields_omitted_when_none(self, nominal, mock_http):
        self._call(nominal, mock_http)
        body = mock_http.post.call_args[1]["json"]
        assert "snils" not in body
        assert "validate_self_employed" not in body
        assert "extra_data" not in body


class TestNominalPayoutSbp:
    def _call(self, nominal, mock_http, **kwargs):
        mock_http.post.return_value = make_response(200, NOMINAL_DATA)
        with patch.object(nominal, "_rsa_headers", return_value={"X-Api-Key": "key", "X-Signature": "sig"}):
            return nominal.payout_sbp(
                transaction="tx-nominal-1",
                amount=100000,
                description="Выплата по договору",
                inn="771234567890",
                kvd="1",
                phone="+79001234567",
                bank_bic="044525225",
                **kwargs,
            )

    def test_returns_nominal_payout(self, nominal, mock_http):
        result = self._call(nominal, mock_http)
        assert isinstance(result, NominalPayout)
        assert result.status == "processing"

    def test_posts_to_correct_path(self, nominal, mock_http):
        self._call(nominal, mock_http)
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/payout/smartcontract/sbp/sber"

    def test_body_contains_required_fields(self, nominal, mock_http):
        self._call(nominal, mock_http)
        body = mock_http.post.call_args[1]["json"]
        assert body["phone"] == "+79001234567"
        assert body["bank_bic"] == "044525225"
        assert body["inn"] == "771234567890"

    def test_optional_fio_check_sent(self, nominal, mock_http):
        self._call(nominal, mock_http, fio="Иванов Иван Иванович", fio_check=True)
        body = mock_http.post.call_args[1]["json"]
        assert body["fio"] == "Иванов Иван Иванович"
        assert body["fio_check"] is True

    def test_optional_fields_omitted_when_none(self, nominal, mock_http):
        self._call(nominal, mock_http)
        body = mock_http.post.call_args[1]["json"]
        assert "fio" not in body
        assert "fio_check" not in body
        assert "extra_data" not in body