from __future__ import annotations

from unittest.mock import patch

import pytest

from sdk_payment_python.models.payout import PayoutCard, PayoutSbp, SbpBank, SbpCheck
from sdk_payment_python.resources.payouts.card import PayoutsCardResource
from sdk_payment_python.resources.payouts.sbp import PayoutsSbpResource
from tests.conftest import BASE_HOST, make_response

PAYOUT_CARD_DATA = {"transaction": "tx-payout", "status": "pending_otp", "amount": 5000}
PAYOUT_SBP_DATA = {"transaction": "tx-sbp", "status": "completed", "amount": 3000}
BANK_DATA = {"id": "bank-1", "name": "Sberbank", "bic": "044525225"}
CHECK_DATA = {"fio": "Иван Иванов", "bank_name": "Sberbank", "success": True}

RSA_PATCH = "sdk_payment_python.utils.KvellUtils.create_rsa_signature"


@pytest.fixture
def payout_card(settings, mock_http):
    return PayoutsCardResource(settings, mock_http, BASE_HOST)


@pytest.fixture
def payout_sbp(settings, mock_http):
    return PayoutsSbpResource(settings, mock_http, BASE_HOST)


class TestPayoutsCardCreate:
    def test_returns_payout_card(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_CARD_DATA)
            result = payout_card.create("tx-payout", 5000, "Payout", "4111111111111111")
            assert isinstance(result, PayoutCard)
            assert result.transaction == "tx-payout"

    def test_posts_to_correct_path(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_CARD_DATA)
            payout_card.create("tx-payout", 5000, "Payout", "4111111111111111")
            assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/account2card"

    def test_body_contains_required_fields(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_CARD_DATA)
            payout_card.create("tx-payout", 5000, "Payout", "4111111111111111")
            body = mock_http.post.call_args[1]["json"]
            assert body["transaction"] == "tx-payout"
            assert body["amount"] == 5000
            assert body["account_number"] == "4111111111111111"

    def test_optional_customer_key_sent(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_CARD_DATA)
            payout_card.create("tx-payout", 5000, "Payout", "4111111111111111", customer_key="cust-1")
            body = mock_http.post.call_args[1]["json"]
            assert body["customer_key"] == "cust-1"

    def test_rsa_signature_used(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig") as mock_rsa:
            mock_http.post.return_value = make_response(200, PAYOUT_CARD_DATA)
            payout_card.create("tx-payout", 5000, "Payout", "4111111111111111")
            assert mock_rsa.called
            headers = mock_http.post.call_args[1]["headers"]
            assert headers["X-Signature"] == "rsa-sig"


class TestPayoutsCardConfirm:
    def test_returns_payout_card(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, {**PAYOUT_CARD_DATA, "status": "completed"})
            result = payout_card.confirm("tx-payout", "123456")
            assert isinstance(result, PayoutCard)
            assert result.status == "completed"

    def test_posts_to_correct_path(self, payout_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_CARD_DATA)
            payout_card.confirm("tx-payout", "123456")
            assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/account2card/confirm"


class TestPayoutsSbpBanks:
    def test_returns_list_of_banks(self, payout_sbp, mock_http):
        mock_http.get.return_value = make_response(200, [BANK_DATA, BANK_DATA])
        result = payout_sbp.banks()
        assert len(result) == 2
        assert all(isinstance(b, SbpBank) for b in result)

    def test_gets_correct_path(self, payout_sbp, mock_http):
        mock_http.get.return_value = make_response(200, [])
        payout_sbp.banks()
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/collections/banks"

    def test_uses_key_only_header(self, payout_sbp, mock_http):
        mock_http.get.return_value = make_response(200, [])
        payout_sbp.banks()
        headers = mock_http.get.call_args[1]["headers"]
        assert "X-Api-Key" in headers
        assert "X-Signature" not in headers

    def test_returns_from_items_key(self, payout_sbp, mock_http):
        mock_http.get.return_value = make_response(200, {"items": [BANK_DATA]})
        result = payout_sbp.banks()
        assert len(result) == 1


class TestPayoutsSbpPhoneBanks:
    def test_returns_list_of_banks(self, payout_sbp, mock_http):
        mock_http.get.return_value = make_response(200, [BANK_DATA])
        result = payout_sbp.phone_banks("+79001234567")
        assert len(result) == 1
        assert isinstance(result[0], SbpBank)

    def test_gets_correct_path(self, payout_sbp, mock_http):
        mock_http.get.return_value = make_response(200, [])
        payout_sbp.phone_banks("+79001234567")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/orders/payout/sbp/banks/+79001234567"


class TestPayoutsSbpCheck:
    def test_returns_sbp_check(self, payout_sbp, mock_http):
        mock_http.post.return_value = make_response(200, CHECK_DATA)
        result = payout_sbp.check("+79001234567", "bank-1")
        assert isinstance(result, SbpCheck)
        assert result.fio == "Иван Иванов"

    def test_posts_to_correct_path(self, payout_sbp, mock_http):
        mock_http.post.return_value = make_response(200, CHECK_DATA)
        payout_sbp.check("+79001234567", "bank-1")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/payout/sbp/check"

    def test_body_has_phone_and_bank_id(self, payout_sbp, mock_http):
        mock_http.post.return_value = make_response(200, CHECK_DATA)
        payout_sbp.check("+79001234567", "bank-1")
        body = mock_http.post.call_args[1]["json"]
        assert body["phone"] == "+79001234567"
        assert body["bank_id"] == "bank-1"

    def test_uses_sha256_signature(self, payout_sbp, mock_http):
        mock_http.post.return_value = make_response(200, CHECK_DATA)
        payout_sbp.check("+79001234567", "bank-1")
        headers = mock_http.post.call_args[1]["headers"]
        assert "X-Signature" in headers
        assert "X-Api-Key" in headers


class TestPayoutsSbpCreate:
    def test_returns_payout_sbp(self, payout_sbp, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_SBP_DATA)
            result = payout_sbp.create("tx-sbp", 3000, "SBP Payout", "+79001234567", "bank-1")
            assert isinstance(result, PayoutSbp)
            assert result.transaction == "tx-sbp"

    def test_posts_to_correct_path(self, payout_sbp, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_SBP_DATA)
            payout_sbp.create("tx-sbp", 3000, "SBP Payout", "+79001234567", "bank-1")
            assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/payout/sbp"

    def test_body_contains_all_required_fields(self, payout_sbp, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_SBP_DATA)
            payout_sbp.create("tx-sbp", 3000, "SBP Payout", "+79001234567", "bank-1")
            body = mock_http.post.call_args[1]["json"]
            assert body["phone"] == "+79001234567"
            assert body["bank_id"] == "bank-1"
            assert body["amount"] == 3000


class TestPayoutsSbpConfirm:
    def test_returns_payout_sbp(self, payout_sbp, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_SBP_DATA)
            result = payout_sbp.confirm("tx-sbp", "654321")
            assert isinstance(result, PayoutSbp)

    def test_posts_to_correct_path(self, payout_sbp, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_SBP_DATA)
            payout_sbp.confirm("tx-sbp", "654321")
            assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/payout/sbp/confirm"
