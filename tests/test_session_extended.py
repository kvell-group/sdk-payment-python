from __future__ import annotations

import pytest

from sdk_payment_python.models.session import SbpResult
from sdk_payment_python.resources.payments.session import SessionResource
from tests.conftest import BASE_HOST, make_response


@pytest.fixture
def session(settings, mock_http):
    return SessionResource(settings, mock_http, BASE_HOST)


class TestSessionSbpB2B:
    def test_returns_sbp_result(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.example.com/b2b"})
        result = session.sbp_b2b("tx-123")
        assert isinstance(result, SbpResult)
        assert result.form_url == "https://sbp.example.com/b2b"

    def test_posts_to_correct_path(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.example.com"})
        session.sbp_b2b("tx-123")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/sbp/b2b"

    def test_body_contains_transaction(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.example.com"})
        session.sbp_b2b("tx-123")
        body = mock_http.post.call_args[1]["json"]
        assert body["transaction"] == "tx-123"

    def test_optional_customer_sent(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.example.com"})
        session.sbp_b2b("tx-123", customer="cust-1")
        body = mock_http.post.call_args[1]["json"]
        assert body["customer"] == "cust-1"

    def test_optional_customer_omitted_by_default(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.example.com"})
        session.sbp_b2b("tx-123")
        body = mock_http.post.call_args[1]["json"]
        assert "customer" not in body
