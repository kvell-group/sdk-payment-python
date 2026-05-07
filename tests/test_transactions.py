import pytest

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources.transactions import TransactionsResource
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
def transactions(settings, mock_http):
    return TransactionsResource(settings, mock_http, BASE_HOST)


class TestTransactionsGet:
    def test_returns_transaction(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, TX_DATA)
        result = transactions.get("tx-123")
        assert isinstance(result, Transaction)
        assert result.transaction == "tx-123"
        assert result.status == "completed"

    def test_gets_correct_path(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, TX_DATA)
        transactions.get("tx-123")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123"


class TestTransactionsRefund:
    def test_full_refund(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "status": "refunded"})
        result = transactions.refund("tx-123")
        assert result.status == "refunded"

    def test_full_refund_sends_empty_body(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "status": "refunded"})
        transactions.refund("tx-123")
        body = mock_http.post.call_args[1]["json"]
        assert body == {}

    def test_partial_refund_sends_amount(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "status": "part_refunded"})
        transactions.refund("tx-123", amount=1000)
        body = mock_http.post.call_args[1]["json"]
        assert body["amount"] == 1000

    def test_posts_to_correct_path(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.refund("tx-123")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123/refund"


class TestTransactionsRebill:
    def test_returns_transaction(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "transaction": "tx-new"})
        result = transactions.rebill("tx-123", "tx-new", 3000, "Rebill")
        assert isinstance(result, Transaction)
        assert result.transaction == "tx-new"

    def test_body_contains_all_fields(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill("tx-parent", "tx-child", 2000, "Recurring")
        body = mock_http.post.call_args[1]["json"]
        assert body["parent_transaction"] == "tx-parent"
        assert body["transaction"] == "tx-child"
        assert body["amount"] == 2000
        assert body["description"] == "Recurring"

    def test_posts_to_correct_path(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill("tx-parent", "tx-child", 2000, "Recurring")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/rebill"
