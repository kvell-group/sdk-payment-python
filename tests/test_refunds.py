import pytest

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources.payments.refunds import RefundsResource
from tests.conftest import BASE_HOST, make_response

TX_DATA = {
    "id": 42,
    "status": "completed",
    "amount": 3000,
    "transaction": "tx-123",
    "description": "Test",
    "created_at": "2024-01-01",
}


@pytest.fixture
def refunds(settings, mock_http):
    return RefundsResource(settings, mock_http, BASE_HOST)


class TestRefunds:
    def test_full_refund(self, refunds, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "status": "refunded"})
        result = refunds.create("tx-123")
        assert isinstance(result, Transaction)
        assert result.status == "refunded"

    def test_full_refund_sends_empty_body(self, refunds, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "status": "refunded"})
        refunds.create("tx-123")
        body = mock_http.post.call_args[1]["json"]
        assert body == {}

    def test_partial_refund_sends_amount(self, refunds, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "status": "part_refunded"})
        refunds.create("tx-123", amount=1000)
        body = mock_http.post.call_args[1]["json"]
        assert body["amount"] == 1000

    def test_posts_to_correct_path(self, refunds, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        refunds.create("tx-123")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123/refund"
