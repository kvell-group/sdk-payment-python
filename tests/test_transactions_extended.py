from __future__ import annotations

import pytest

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources.payments.transactions import TransactionsResource
from tests.conftest import BASE_HOST, make_response

BAAS_HOST = "https://api.baas.kvell.group"
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
    return TransactionsResource(settings, mock_http, BASE_HOST, BAAS_HOST)


class TestTransactionsRebillExtended:
    def test_rebill_with_fiscal_data(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill("tx-parent", "tx-child", 2000, "Recurring", fiscal_data={"vat": 20})
        body = mock_http.post.call_args[1]["json"]
        assert body["fiscal_data"] == {"vat": 20}

    def test_rebill_with_extra_data(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill("tx-parent", "tx-child", 2000, "Recurring", extra_data={"order_id": "99"})
        body = mock_http.post.call_args[1]["json"]
        assert body["extra_data"] == {"order_id": "99"}

    def test_rebill_without_optional_fields(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill("tx-parent", "tx-child", 2000, "Recurring")
        body = mock_http.post.call_args[1]["json"]
        assert "fiscal_data" not in body
        assert "extra_data" not in body


class TestTransactionsRebillFromProfile:
    def test_returns_transaction(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "transaction": "tx-new"})
        result = transactions.rebill_from_profile("tx-parent", "tx-new", 3000, "Rebill", "cust-1")
        assert isinstance(result, Transaction)
        assert result.transaction == "tx-new"

    def test_body_contains_customer_key(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill_from_profile("tx-parent", "tx-child", 2000, "Rebill", "cust-1")
        body = mock_http.post.call_args[1]["json"]
        assert body["customer_key"] == "cust-1"

    def test_posts_to_correct_path(self, transactions, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        transactions.rebill_from_profile("tx-parent", "tx-child", 2000, "Rebill", "cust-1")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/rebill-from-profile"


class TestTransactionsList:
    def test_returns_list_of_transactions(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, [TX_DATA, TX_DATA])
        result = transactions.list()
        assert len(result) == 2
        assert all(isinstance(t, Transaction) for t in result)

    def test_returns_list_from_items_key(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, {"items": [TX_DATA], "total": 1})
        result = transactions.list()
        assert len(result) == 1

    def test_sends_page_and_size(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, [])
        transactions.list(page=2, size=50)
        params = mock_http.get.call_args[1]["params"]
        assert params["page"] == 2
        assert params["size"] == 50

    def test_sends_status_filter(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, [])
        transactions.list(status="completed")
        params = mock_http.get.call_args[1]["params"]
        assert params["status"] == "completed"

    def test_sends_date_filters(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, [])
        transactions.list(date_from="2024-01-01", date_to="2024-12-31")
        params = mock_http.get.call_args[1]["params"]
        assert params["date_from"] == "2024-01-01"
        assert params["date_to"] == "2024-12-31"

    def test_request_id_header_set(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, [])
        transactions.list()
        headers = mock_http.get.call_args[1]["headers"]
        assert "X-Request-Id" in headers

    def test_uses_baas_host(self, transactions, mock_http):
        mock_http.get.return_value = make_response(200, [])
        transactions.list()
        url = mock_http.get.call_args[0][0]
        assert url == f"{BAAS_HOST}/v1/orders"
