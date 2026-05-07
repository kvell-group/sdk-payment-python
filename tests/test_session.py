import pytest

from sdk_payment_python.exceptions import KvellAPIError, KvellValidationError
from sdk_payment_python.models.session import AlfaPayResult, SessionCreated, SbpResult
from sdk_payment_python.resources.payments.session import SessionResource
from tests.conftest import API_KEY, BASE_HOST, make_response


@pytest.fixture
def session(settings, mock_http):
    return SessionResource(settings, mock_http, BASE_HOST)


class TestSessionCreate:
    def test_returns_session_created(self, session, mock_http):
        mock_http.post.return_value = make_response(201, {"ok": True})
        result = session.create(amount=1000, transaction="tx-1", description="Test")
        assert isinstance(result, SessionCreated)
        assert result.ok is True

    def test_posts_to_correct_path(self, session, mock_http):
        mock_http.post.return_value = make_response(201, {"ok": True})
        session.create(amount=1000, transaction="tx-1", description="Test")
        url = mock_http.post.call_args[0][0]
        assert url == f"{BASE_HOST}/v1/orders/session"

    def test_body_contains_required_fields(self, session, mock_http):
        mock_http.post.return_value = make_response(201, {"ok": True})
        session.create(amount=1000, transaction="tx-1", description="Test")
        body = mock_http.post.call_args[1]["json"]
        assert body["amount"] == 1000
        assert body["transaction"] == "tx-1"
        assert body["description"] == "Test"

    def test_auth_headers_sent(self, session, mock_http):
        mock_http.post.return_value = make_response(201, {"ok": True})
        session.create(amount=1000, transaction="tx-1", description="Test")
        headers = mock_http.post.call_args[1]["headers"]
        assert headers["X-Api-Key"] == API_KEY
        assert "X-Signature" in headers

    def test_optional_extra_data_included(self, session, mock_http):
        mock_http.post.return_value = make_response(201, {"ok": True})
        session.create(amount=1000, transaction="tx-1", description="Test", extra_data={"ref": "abc"})
        body = mock_http.post.call_args[1]["json"]
        assert body["extra_data"] == {"ref": "abc"}

    def test_422_raises_validation_error(self, session, mock_http):
        mock_http.post.return_value = make_response(422, {"errors": [{"message": "Bad amount", "code": 1}]})
        with pytest.raises(KvellValidationError) as exc_info:
            session.create(amount=-1, transaction="tx-1", description="Test")
        assert exc_info.value.errors[0]["message"] == "Bad amount"

    def test_500_raises_api_error(self, session, mock_http):
        mock_http.post.return_value = make_response(500, {})
        with pytest.raises(KvellAPIError) as exc_info:
            session.create(amount=1000, transaction="tx-1", description="Test")
        assert exc_info.value.status_code == 500


class TestSessionSbp:
    def test_returns_sbp_result(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.link"})
        result = session.sbp(transaction="tx-1")
        assert isinstance(result, SbpResult)
        assert result.form_url == "https://sbp.link"

    def test_posts_to_correct_path(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.link"})
        session.sbp(transaction="tx-1")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/sbp"

    def test_optional_customer_included(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.link"})
        session.sbp(transaction="tx-1", customer="user@example.com")
        body = mock_http.post.call_args[1]["json"]
        assert body["customer"] == "user@example.com"

    def test_optional_customer_excluded_when_none(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://sbp.link"})
        session.sbp(transaction="tx-1")
        body = mock_http.post.call_args[1]["json"]
        assert "customer" not in body


class TestSessionAlfaPay:
    def test_returns_alfapay_result(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://alfa.link"})
        result = session.alfapay(transaction="tx-1", ip="127.0.0.1")
        assert isinstance(result, AlfaPayResult)
        assert result.form_url == "https://alfa.link"

    def test_body_contains_ip(self, session, mock_http):
        mock_http.post.return_value = make_response(200, {"form_url": "https://alfa.link"})
        session.alfapay(transaction="tx-1", ip="127.0.0.1")
        body = mock_http.post.call_args[1]["json"]
        assert body["ip"] == "127.0.0.1"
