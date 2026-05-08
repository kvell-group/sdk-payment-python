from __future__ import annotations

from unittest.mock import patch

import pytest

from sdk_payment_python.models.issue_card import IssueCardApplication, IssueCardDocs, IssueCardPayout, IssueCardResult
from sdk_payment_python.resources.issue_card.issue_card import IssueCardResource
from tests.conftest import BASE_HOST, make_response

API_HOST = "http://api.pay.kvell.group"

APP_DATA = {"id": "app-123", "status": "pending", "request_id": "req-001"}
DOCS_DATA = {"url": "https://example.com/docs/sign"}
RESULT_DATA = {"id": "res-123", "status": "completed", "card_mask": "411111******1111"}
PAYOUT_DATA = {"id": 99, "status": "completed", "amount": 10000}

RSA_PATCH = "sdk_payment_python.utils.KvellUtils.create_rsa_signature"
JSON_SIG_PATCH = "sdk_payment_python.utils.KvellUtils.create_signature_by_json_body"


@pytest.fixture
def issue_card(settings, mock_http):
    return IssueCardResource(settings, mock_http, BASE_HOST, API_HOST)


class TestIssueCardCreate:
    def test_returns_application(self, issue_card, mock_http):
        with patch(JSON_SIG_PATCH, return_value="json-sig"):
            mock_http.post.return_value = make_response(200, APP_DATA)
            result = issue_card.create("req-001", {"name": "Иван"})
            assert isinstance(result, IssueCardApplication)
            assert result.request_id == "req-001"

    def test_posts_to_correct_path(self, issue_card, mock_http):
        with patch(JSON_SIG_PATCH, return_value="json-sig"):
            mock_http.post.return_value = make_response(200, APP_DATA)
            issue_card.create("req-001", {"name": "Иван"})
            assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/issue-card/applications"

    def test_body_contains_request_id_and_additional_data(self, issue_card, mock_http):
        with patch(JSON_SIG_PATCH, return_value="json-sig"):
            mock_http.post.return_value = make_response(200, APP_DATA)
            issue_card.create("req-001", {"name": "Иван"})
            body = mock_http.post.call_args[1]["json"]
            assert body["request_id"] == "req-001"
            assert body["additional_data"] == {"name": "Иван"}

    def test_uses_json_body_signature(self, issue_card, mock_http):
        with patch(JSON_SIG_PATCH, return_value="json-sig") as mock_sig:
            mock_http.post.return_value = make_response(200, APP_DATA)
            issue_card.create("req-001", {"name": "Иван"})
            assert mock_sig.called
            headers = mock_http.post.call_args[1]["headers"]
            assert headers["X-Signature"] == "json-sig"


class TestIssueCardDocs:
    def test_returns_issue_card_docs(self, issue_card, mock_http):
        mock_http.get.return_value = make_response(200, DOCS_DATA)
        result = issue_card.docs("app-123")
        assert isinstance(result, IssueCardDocs)
        assert result.url == "https://example.com/docs/sign"

    def test_gets_correct_path(self, issue_card, mock_http):
        mock_http.get.return_value = make_response(200, DOCS_DATA)
        issue_card.docs("app-123")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/issue-card/applications/app-123/docs"

    def test_uses_sha256_signature(self, issue_card, mock_http):
        mock_http.get.return_value = make_response(200, DOCS_DATA)
        issue_card.docs("app-123")
        headers = mock_http.get.call_args[1]["headers"]
        assert "X-Signature" in headers


class TestIssueCardIssue:
    def test_returns_issue_card_result(self, issue_card, mock_http):
        mock_http.post.return_value = make_response(200, RESULT_DATA)
        result = issue_card.issue("app-123")
        assert isinstance(result, IssueCardResult)
        assert result.status == "completed"

    def test_posts_to_correct_path(self, issue_card, mock_http):
        mock_http.post.return_value = make_response(200, RESULT_DATA)
        issue_card.issue("app-123")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/issue-card/applications/app-123/issue"

    def test_uses_sha256_signature(self, issue_card, mock_http):
        mock_http.post.return_value = make_response(200, RESULT_DATA)
        issue_card.issue("app-123")
        headers = mock_http.post.call_args[1]["headers"]
        assert "X-Signature" in headers


class TestIssueCardPayout:
    def test_returns_issue_card_payout(self, issue_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_DATA)
            result = issue_card.payout("card-1", 10000, "tx-001", "Выплата")
            assert isinstance(result, IssueCardPayout)
            assert result.amount == 10000

    def test_posts_to_api_host(self, issue_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_DATA)
            issue_card.payout("card-1", 10000, "tx-001", "Выплата")
            assert mock_http.post.call_args[0][0] == f"{API_HOST}/v1/orders/payout/issue-card"

    def test_body_contains_required_fields(self, issue_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_DATA)
            issue_card.payout("card-1", 10000, "tx-001", "Выплата")
            body = mock_http.post.call_args[1]["json"]
            assert body["card_id"] == "card-1"
            assert body["amount"] == 10000
            assert body["transaction"] == "tx-001"
            assert body["description"] == "Выплата"

    def test_optional_fiscal_data_sent(self, issue_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig"):
            mock_http.post.return_value = make_response(200, PAYOUT_DATA)
            issue_card.payout("card-1", 10000, "tx-001", "Выплата", fiscal_data={"inn": "123"})
            body = mock_http.post.call_args[1]["json"]
            assert body["fiscal_data"] == {"inn": "123"}

    def test_uses_rsa_signature(self, issue_card, mock_http):
        with patch(RSA_PATCH, return_value="rsa-sig") as mock_rsa:
            mock_http.post.return_value = make_response(200, PAYOUT_DATA)
            issue_card.payout("card-1", 10000, "tx-001", "Выплата")
            assert mock_rsa.called
            headers = mock_http.post.call_args[1]["headers"]
            assert headers["X-Signature"] == "rsa-sig"
