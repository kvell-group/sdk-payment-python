import json
from urllib.parse import parse_qs, urlparse

import pytest

from sdk_payment_python.resources.payments.checkout import CheckoutResource
from sdk_payment_python.utils import KvellUtils
from tests.conftest import API_KEY, CHECKOUT_HOST, SECRET_KEY, make_response


@pytest.fixture
def checkout(settings, mock_http):
    return CheckoutResource(settings, mock_http, CHECKOUT_HOST)


REQUIRED = {
    "amount": 1000,
    "transaction": "tx-123",
    "description": "Test payment",
    "success_url": "https://example.com/success",
    "fail_url": "https://example.com/fail",
}


class TestBuildUrl:
    def test_url_structure(self, checkout):
        url = checkout.build_url(**REQUIRED)
        parsed = urlparse(url)
        assert parsed.scheme == "https"
        assert parsed.netloc == "pay.kvell.group"
        assert parsed.path == "/checkout"

    def test_required_params_present(self, checkout):
        url = checkout.build_url(**REQUIRED)
        qs = parse_qs(urlparse(url).query)
        assert qs["api_key"] == [API_KEY]
        assert qs["amount"] == ["1000"]
        assert qs["transaction"] == ["tx-123"]
        assert qs["signature"]

    def test_signature_correctness(self, checkout):
        url = checkout.build_url(**REQUIRED)
        qs = parse_qs(urlparse(url).query)
        expected = KvellUtils.create_signature(API_KEY, SECRET_KEY, ["tx-123", 1000])
        assert qs["signature"] == [expected]

    def test_signature_with_expires_at(self, checkout):
        url = checkout.build_url(**REQUIRED, expires_at=9999999999)
        qs = parse_qs(urlparse(url).query)
        expected = KvellUtils.create_signature(API_KEY, SECRET_KEY, ["tx-123", 1000, 9999999999])
        assert qs["signature"] == [expected]
        assert qs["expires_at"] == ["9999999999"]

    def test_optional_phone_included(self, checkout):
        url = checkout.build_url(**REQUIRED, phone="+79001234567")
        assert "phone=" in url

    def test_optional_phone_excluded_when_none(self, checkout):
        url = checkout.build_url(**REQUIRED)
        assert "phone" not in urlparse(url).query

    def test_auto_return(self, checkout):
        url = checkout.build_url(**REQUIRED, auto_return=5)
        assert "auto_return=5" in url

    def test_extra_data_json_encoded_in_url(self, checkout):
        url = checkout.build_url(**REQUIRED, extra_data={"order_id": 42})
        qs = parse_qs(urlparse(url).query)
        assert json.loads(qs["extra_data"][0]) == {"order_id": 42}

    def test_fiscal_data_json_encoded_in_url(self, checkout):
        url = checkout.build_url(**REQUIRED, fiscal_data={"inn": "123456789012"})
        qs = parse_qs(urlparse(url).query)
        assert json.loads(qs["fiscal_data"][0]) == {"inn": "123456789012"}

    def test_split_data_json_encoded_in_url(self, checkout):
        url = checkout.build_url(**REQUIRED, split_data=[{"amount": 100, "transaction": "tx-sub"}])
        qs = parse_qs(urlparse(url).query)
        assert json.loads(qs["split_data"][0]) == [{"amount": 100, "transaction": "tx-sub"}]


class TestBuildFormFields:
    def test_returns_dict_with_required_keys(self, checkout):
        fields = checkout.build_form_fields(**REQUIRED)
        assert all(k in fields for k in ("api_key", "amount", "transaction", "signature"))

    def test_extra_data_json_encoded_in_form_fields(self, checkout):
        fields = checkout.build_form_fields(**REQUIRED, extra_data={"order_id": 42})
        assert json.loads(fields["extra_data"]) == {"order_id": 42}

    def test_fiscal_data_json_encoded_in_form_fields(self, checkout):
        fields = checkout.build_form_fields(**REQUIRED, fiscal_data={"inn": "123456789012"})
        assert json.loads(fields["fiscal_data"]) == {"inn": "123456789012"}

    def test_split_data_json_encoded_in_form_fields(self, checkout):
        fields = checkout.build_form_fields(**REQUIRED, split_data=[{"amount": 100, "transaction": "tx-sub"}])
        assert json.loads(fields["split_data"]) == [{"amount": 100, "transaction": "tx-sub"}]

    def test_optional_not_included_when_none(self, checkout):
        fields = checkout.build_form_fields(**REQUIRED)
        assert "phone" not in fields
        assert "extra_data" not in fields


class TestCreate:
    def test_returns_url_from_response(self, checkout, mock_http):
        mock_http.post.return_value = make_response(200, {"url": "https://pay.kvell.group/checkout/orders/abc"})
        result = checkout.create(**REQUIRED)
        assert result == "https://pay.kvell.group/checkout/orders/abc"

    def test_posts_to_correct_path(self, checkout, mock_http):
        mock_http.post.return_value = make_response(200, {"url": "https://pay.kvell.group/checkout/orders/abc"})
        checkout.create(**REQUIRED)
        call_args = mock_http.post.call_args
        assert call_args[0][0] == f"{CHECKOUT_HOST}/checkout"

    def test_includes_accept_json_header(self, checkout, mock_http):
        mock_http.post.return_value = make_response(200, {"url": "https://x"})
        checkout.create(**REQUIRED)
        headers = mock_http.post.call_args[1]["headers"]
        assert headers.get("Accept") == "application/json"
