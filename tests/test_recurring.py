import pytest

from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources.payments.recurring import RecurringResource
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
def recurring(settings, mock_http):
    return RecurringResource(settings, mock_http, BASE_HOST)


class TestRebill:
    def test_returns_transaction(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "transaction": "tx-new"})
        result = recurring.rebill("tx-123", "tx-new", 3000, "Rebill")
        assert isinstance(result, Transaction)
        assert result.transaction == "tx-new"

    def test_body_contains_all_fields(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill("tx-parent", "tx-child", 2000, "Recurring")
        body = mock_http.post.call_args[1]["json"]
        assert body["parent_transaction"] == "tx-parent"
        assert body["transaction"] == "tx-child"
        assert body["amount"] == 2000
        assert body["description"] == "Recurring"

    def test_posts_to_correct_path(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill("tx-parent", "tx-child", 2000, "Recurring")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/rebill"

    def test_with_fiscal_data(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill("tx-parent", "tx-child", 2000, "Recurring", fiscal_data={"vat": 20})
        body = mock_http.post.call_args[1]["json"]
        assert body["fiscal_data"] == {"vat": 20}

    def test_with_extra_data(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill("tx-parent", "tx-child", 2000, "Recurring", extra_data={"order_id": "99"})
        body = mock_http.post.call_args[1]["json"]
        assert body["extra_data"] == {"order_id": "99"}

    def test_without_optional_fields(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill("tx-parent", "tx-child", 2000, "Recurring")
        body = mock_http.post.call_args[1]["json"]
        assert "fiscal_data" not in body
        assert "extra_data" not in body


class TestRebillFromProfile:
    def test_returns_transaction(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, {**TX_DATA, "transaction": "tx-new"})
        result = recurring.rebill_from_profile("tx-parent", "tx-new", 3000, "Rebill", "cust-1")
        assert isinstance(result, Transaction)
        assert result.transaction == "tx-new"

    def test_body_contains_customer_key(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill_from_profile("tx-parent", "tx-child", 2000, "Rebill", "cust-1")
        body = mock_http.post.call_args[1]["json"]
        assert body["customer_key"] == "cust-1"

    def test_posts_to_correct_path(self, recurring, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        recurring.rebill_from_profile("tx-parent", "tx-child", 2000, "Rebill", "cust-1")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/rebill-from-profile"
