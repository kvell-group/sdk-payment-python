from __future__ import annotations

import pytest

from sdk_payment_python.models.smz import InnCheck, SmzClient, SmzReceipt
from sdk_payment_python.resources.smz.smz import SmzResource
from tests.conftest import BASE_HOST, make_response

INN_CHECK_DATA = {"status": "active", "message": "ИП зарегистрирован"}
CLIENT_DATA = {
    "id": 1,
    "inn": "123456789012",
    "first_name": "Иван",
    "last_name": "Иванов",
    "email": "ivan@example.com",
    "phone": "+79001234567",
}
RECEIPT_DATA = {
    "id": 10,
    "inn": "123456789012",
    "amount": 5000,
    "service_name": "Консультация",
    "status": "pending",
}


@pytest.fixture
def smz(settings, mock_http):
    return SmzResource(settings, mock_http, BASE_HOST)


class TestSmzInnCheck:
    def test_returns_inn_check(self, smz, mock_http):
        mock_http.get.return_value = make_response(200, INN_CHECK_DATA)
        result = smz.inn_check("123456789012")
        assert isinstance(result, InnCheck)
        assert result.status == "active"

    def test_gets_correct_path(self, smz, mock_http):
        mock_http.get.return_value = make_response(200, INN_CHECK_DATA)
        smz.inn_check("123456789012")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/smz/inn/check"

    def test_passes_inn_as_param(self, smz, mock_http):
        mock_http.get.return_value = make_response(200, INN_CHECK_DATA)
        smz.inn_check("123456789012")
        params = mock_http.get.call_args[1]["params"]
        assert params["inn"] == "123456789012"

    def test_uses_sha256_signature(self, smz, mock_http):
        mock_http.get.return_value = make_response(200, INN_CHECK_DATA)
        smz.inn_check("123456789012")
        headers = mock_http.get.call_args[1]["headers"]
        assert "X-Signature" in headers


class TestSmzCreate:
    def test_returns_smz_client(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, CLIENT_DATA)
        result = smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567")
        assert isinstance(result, SmzClient)
        assert result.inn == "123456789012"

    def test_posts_to_correct_path(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, CLIENT_DATA)
        smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/smz/clients"

    def test_body_contains_required_fields(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, CLIENT_DATA)
        smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567")
        body = mock_http.post.call_args[1]["json"]
        assert body["inn"] == "123456789012"
        assert body["first_name"] == "Иван"
        assert body["last_name"] == "Иванов"
        assert body["email"] == "ivan@example.com"
        assert body["phone"] == "+79001234567"

    def test_optional_second_name_sent(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, CLIENT_DATA)
        smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567", second_name="Петрович")
        body = mock_http.post.call_args[1]["json"]
        assert body["second_name"] == "Петрович"

    def test_optional_second_name_omitted_when_none(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, CLIENT_DATA)
        smz.create("123456789012", "Иван", "Иванов", "ivan@example.com", "+79001234567")
        body = mock_http.post.call_args[1]["json"]
        assert "second_name" not in body


class TestSmzReceiptCreate:
    def test_returns_smz_receipt(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, RECEIPT_DATA)
        result = smz.receipt_create("123456789012", 5000, "Консультация")
        assert isinstance(result, SmzReceipt)
        assert result.amount == 5000

    def test_posts_to_correct_path(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, RECEIPT_DATA)
        smz.receipt_create("123456789012", 5000, "Консультация")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/smz/receipts"

    def test_body_contains_required_fields(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, RECEIPT_DATA)
        smz.receipt_create("123456789012", 5000, "Консультация")
        body = mock_http.post.call_args[1]["json"]
        assert body["inn"] == "123456789012"
        assert body["amount"] == 5000
        assert body["service_name"] == "Консультация"

    def test_optional_description_sent(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, RECEIPT_DATA)
        smz.receipt_create("123456789012", 5000, "Консультация", description="Доп. инфо")
        body = mock_http.post.call_args[1]["json"]
        assert body["description"] == "Доп. инфо"


class TestSmzReceiptGet:
    def test_returns_smz_receipt(self, smz, mock_http):
        mock_http.get.return_value = make_response(200, RECEIPT_DATA)
        result = smz.receipt_get(10)
        assert isinstance(result, SmzReceipt)
        assert result.id == 10

    def test_gets_correct_path(self, smz, mock_http):
        mock_http.get.return_value = make_response(200, RECEIPT_DATA)
        smz.receipt_get(10)
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/smz/receipts/10"


class TestSmzReceiptCancel:
    def test_returns_smz_receipt(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, {**RECEIPT_DATA, "status": "cancelled"})
        result = smz.receipt_cancel(10)
        assert isinstance(result, SmzReceipt)
        assert result.status == "cancelled"

    def test_posts_to_correct_path(self, smz, mock_http):
        mock_http.post.return_value = make_response(200, RECEIPT_DATA)
        smz.receipt_cancel(10)
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/smz/receipts/10/cancel"
