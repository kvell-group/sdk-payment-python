from __future__ import annotations

import pytest

from sdk_payment_python.models.customer import Customer, CustomerCard
from sdk_payment_python.models.transaction import Transaction
from sdk_payment_python.resources.customers import CustomersResource
from tests.conftest import BASE_HOST, make_response

CUSTOMER_HOST = "https://customer.pay.kvell.group"
CUSTOMER_DATA = {"customer_key": "cust-abc", "email": "user@example.com", "name": "Ivan"}
CARD_DATA = {"id": 10, "card_token": "tok-xyz", "pan": "411111******1111", "brand": "VISA"}
TX_DATA = {
    "id": 42,
    "status": "completed",
    "amount": 2000,
    "transaction": "tx-cust",
    "description": "Card pay",
    "created_at": "2024-01-01",
}


@pytest.fixture
def customers(settings, mock_http):
    return CustomersResource(settings, mock_http, BASE_HOST, CUSTOMER_HOST)


class TestCustomersCreate:
    def test_returns_customer(self, customers, mock_http):
        mock_http.post.return_value = make_response(201, CUSTOMER_DATA)
        result = customers.create("cust-abc", email="user@example.com")
        assert isinstance(result, Customer)
        assert result.customer_key == "cust-abc"

    def test_posts_to_correct_path(self, customers, mock_http):
        mock_http.post.return_value = make_response(201, CUSTOMER_DATA)
        customers.create("cust-abc")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/customers"

    def test_body_has_customer_key(self, customers, mock_http):
        mock_http.post.return_value = make_response(201, CUSTOMER_DATA)
        customers.create("cust-abc", name="Ivan")
        body = mock_http.post.call_args[1]["json"]
        assert body["customer_key"] == "cust-abc"
        assert body["name"] == "Ivan"

    def test_optional_fields_omitted_when_none(self, customers, mock_http):
        mock_http.post.return_value = make_response(201, CUSTOMER_DATA)
        customers.create("cust-abc")
        body = mock_http.post.call_args[1]["json"]
        assert "email" not in body
        assert "phone" not in body
        assert "name" not in body


class TestCustomersGet:
    def test_returns_customer(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, CUSTOMER_DATA)
        result = customers.get("cust-abc")
        assert isinstance(result, Customer)
        assert result.customer_key == "cust-abc"

    def test_gets_correct_path(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, CUSTOMER_DATA)
        customers.get("cust-abc")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/customers/cust-abc"


class TestCustomersUpdate:
    def test_returns_updated_customer(self, customers, mock_http):
        mock_http.patch.return_value = make_response(200, {**CUSTOMER_DATA, "name": "Petr"})
        result = customers.update("cust-abc", name="Petr")
        assert isinstance(result, Customer)

    def test_patches_correct_path(self, customers, mock_http):
        mock_http.patch.return_value = make_response(200, CUSTOMER_DATA)
        customers.update("cust-abc", email="new@example.com")
        assert mock_http.patch.call_args[0][0] == f"{BASE_HOST}/v1/customers/cust-abc"


class TestCustomersList:
    def test_returns_list_of_customers(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, [CUSTOMER_DATA])
        result = customers.list()
        assert len(result) == 1
        assert isinstance(result[0], Customer)

    def test_returns_from_items_key(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, {"items": [CUSTOMER_DATA, CUSTOMER_DATA]})
        result = customers.list()
        assert len(result) == 2

    def test_sends_page_and_size(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, [])
        customers.list(page=3, size=10)
        params = mock_http.get.call_args[1]["params"]
        assert params["page"] == 3
        assert params["size"] == 10


class TestCustomersCardsList:
    def test_returns_list_of_cards(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, [CARD_DATA])
        result = customers.cards_list("cust-abc")
        assert len(result) == 1
        assert isinstance(result[0], CustomerCard)
        assert result[0].card_token == "tok-xyz"

    def test_gets_correct_path(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, [])
        customers.cards_list("cust-abc")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/customers/cust-abc/cards"


class TestCustomersCardGet:
    def test_returns_card(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, CARD_DATA)
        result = customers.card_get("cust-abc", 10)
        assert isinstance(result, CustomerCard)
        assert result.id == 10

    def test_gets_correct_path(self, customers, mock_http):
        mock_http.get.return_value = make_response(200, CARD_DATA)
        customers.card_get("cust-abc", 10)
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/customers/cust-abc/cards/10"


class TestCustomersCardDelete:
    def test_calls_delete(self, customers, mock_http):
        mock_http.delete.return_value = make_response(204, {})
        customers.card_delete("cust-abc", 10)
        assert mock_http.delete.called

    def test_deletes_correct_path(self, customers, mock_http):
        mock_http.delete.return_value = make_response(204, {})
        customers.card_delete("cust-abc", 10)
        assert mock_http.delete.call_args[0][0] == f"{BASE_HOST}/v1/customers/cust-abc/cards/10"


class TestCustomersCardBindUrl:
    def test_returns_string_url(self, customers):
        url = customers.card_bind_url("cust-abc")
        assert isinstance(url, str)
        assert CUSTOMER_HOST in url
        assert "cust-abc" in url

    def test_url_starts_with_customer_host(self, customers):
        url = customers.card_bind_url("cust-abc")
        assert url.startswith(CUSTOMER_HOST)


class TestCustomersCardPayment:
    def test_returns_transaction(self, customers, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        result = customers.card_payment("cust-abc", "tok-xyz", "tx-cust", 2000, "Card pay")
        assert isinstance(result, Transaction)
        assert result.transaction == "tx-cust"

    def test_posts_to_correct_path(self, customers, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        customers.card_payment("cust-abc", "tok-xyz", "tx-cust", 2000, "Card pay")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/customers/cards/pay"

    def test_body_has_required_fields(self, customers, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        customers.card_payment("cust-abc", "tok-xyz", "tx-cust", 2000, "Card pay")
        body = mock_http.post.call_args[1]["json"]
        assert body["customer_key"] == "cust-abc"
        assert body["card_token"] == "tok-xyz"
        assert body["transaction"] == "tx-cust"
        assert body["amount"] == 2000


class TestCustomersCardPayout:
    def test_returns_transaction(self, customers, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        result = customers.card_payout("cust-abc", "tok-xyz", "tx-cust", 2000, "Card payout")
        assert isinstance(result, Transaction)

    def test_posts_to_correct_path(self, customers, mock_http):
        mock_http.post.return_value = make_response(200, TX_DATA)
        customers.card_payout("cust-abc", "tok-xyz", "tx-cust", 2000, "Card payout")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/customers/cards/payout"
