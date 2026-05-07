from __future__ import annotations

import pytest

from sdk_payment_python.models.draft import PayoutDraft
from sdk_payment_python.resources.payouts.drafts import PayoutDraftsResource
from tests.conftest import BASE_HOST, make_response

DRAFT_DATA = {
    "id": 42,
    "status": "pending",
    "payout_type": "sbp",
    "amount": 10000,
    "description": "Test draft",
}


@pytest.fixture
def drafts(settings, mock_http):
    return PayoutDraftsResource(settings, mock_http, BASE_HOST)


class TestDraftCreate:
    def test_returns_payout_draft(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        result = drafts.create("sbp", 10000, "Test draft")
        assert isinstance(result, PayoutDraft)
        assert result.amount == 10000

    def test_posts_to_correct_path(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.create("sbp", 10000, "Test draft")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/payout-drafts"

    def test_body_contains_required_fields(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.create("sbp", 10000, "Test draft")
        body = mock_http.post.call_args[1]["json"]
        assert body["payout_type"] == "sbp"
        assert body["amount"] == 10000
        assert body["description"] == "Test draft"

    def test_optional_recipient_phone_sent(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.create("sbp", 10000, "Test draft", recipient_phone="+79001234567")
        body = mock_http.post.call_args[1]["json"]
        assert body["recipient_phone"] == "+79001234567"

    def test_optional_recipient_phone_not_sent_when_none(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.create("sbp", 10000, "Test draft")
        body = mock_http.post.call_args[1]["json"]
        assert "recipient_phone" not in body


class TestDraftConfirm:
    def test_returns_payout_draft(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, {**DRAFT_DATA, "status": "confirmed"})
        result = drafts.confirm(42)
        assert isinstance(result, PayoutDraft)
        assert result.status == "confirmed"

    def test_posts_to_correct_path(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.confirm(42)
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/payout-drafts/42/confirm"

    def test_uses_sha256_signature(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.confirm(42)
        headers = mock_http.post.call_args[1]["headers"]
        assert "X-Signature" in headers


class TestDraftConfirmByNumber:
    def test_posts_to_correct_path(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        drafts.confirm_by_number("DRAFT-001")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/payout-drafts/number/DRAFT-001/confirm"

    def test_returns_payout_draft(self, drafts, mock_http):
        mock_http.post.return_value = make_response(200, DRAFT_DATA)
        result = drafts.confirm_by_number("DRAFT-001")
        assert isinstance(result, PayoutDraft)


class TestDraftGet:
    def test_returns_payout_draft(self, drafts, mock_http):
        mock_http.get.return_value = make_response(200, DRAFT_DATA)
        result = drafts.get(42)
        assert isinstance(result, PayoutDraft)
        assert result.id == 42

    def test_gets_correct_path(self, drafts, mock_http):
        mock_http.get.return_value = make_response(200, DRAFT_DATA)
        drafts.get(42)
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/payout-drafts/42"


class TestDraftGetByNumber:
    def test_returns_payout_draft(self, drafts, mock_http):
        mock_http.get.return_value = make_response(200, DRAFT_DATA)
        result = drafts.get_by_number("DRAFT-001")
        assert isinstance(result, PayoutDraft)

    def test_gets_correct_path(self, drafts, mock_http):
        mock_http.get.return_value = make_response(200, DRAFT_DATA)
        drafts.get_by_number("DRAFT-001")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/payout-drafts/number/DRAFT-001"
