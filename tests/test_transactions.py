import pytest

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources.payments.transactions import TransactionsResource
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
