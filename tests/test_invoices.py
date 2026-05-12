from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from sdk_payment_python.exceptions import KvellValidationError
from sdk_payment_python.models.invoice import Invoice
from sdk_payment_python.resources.payments.invoices import AsyncInvoicesResource, InvoicesResource
from tests.conftest import API_KEY, BASE_HOST, make_response

INVOICE_DATA = {
    "invoice_guid": "guid-abc",
    "status": "new",
    "amount": 5000,
    "url": "https://pay.kvell.group/inv/abc",
    "created_at": "2024-01-01",
    "expired_at": "2024-01-02",
    "invoice_number": "INV-001",
}


@pytest.fixture
def invoices(settings, mock_http):
    return InvoicesResource(settings, mock_http, BASE_HOST)


class TestInvoicesCreate:
    def test_returns_invoice(self, invoices, mock_http):
        mock_http.post.return_value = make_response(201, INVOICE_DATA)
        result = invoices.create(invoice_number="INV-001", amount=5000, description="Test")
        assert isinstance(result, Invoice)
        assert result.invoice_guid == "guid-abc"
        assert result.status == "new"

    def test_posts_to_correct_path(self, invoices, mock_http):
        mock_http.post.return_value = make_response(201, INVOICE_DATA)
        invoices.create(invoice_number="INV-001", amount=5000, description="Test")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/invoices"

    def test_422_raises_validation_error(self, invoices, mock_http):
        mock_http.post.return_value = make_response(422, {"errors": [{"message": "Dup number", "code": 2}]})
        with pytest.raises(KvellValidationError):
            invoices.create(invoice_number="INV-001", amount=5000, description="Test")


class TestInvoicesGet:
    def test_returns_invoice(self, invoices, mock_http):
        mock_http.get.return_value = make_response(200, INVOICE_DATA)
        result = invoices.get("guid-abc")
        assert isinstance(result, Invoice)
        assert result.invoice_guid == "guid-abc"

    def test_gets_correct_path(self, invoices, mock_http):
        mock_http.get.return_value = make_response(200, INVOICE_DATA)
        invoices.get("guid-abc")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/invoices/guid-abc"

    def test_only_api_key_header(self, invoices, mock_http):
        mock_http.get.return_value = make_response(200, INVOICE_DATA)
        invoices.get("guid-abc")
        headers = mock_http.get.call_args[1]["headers"]
        assert headers["X-Api-Key"] == API_KEY
        assert "X-Signature" not in headers


class TestInvoicesCancel:
    def test_returns_canceled_invoice(self, invoices, mock_http):
        mock_http.patch.return_value = make_response(200, {**INVOICE_DATA, "status": "canceled"})
        result = invoices.cancel("guid-abc")
        assert result.status == "canceled"

    def test_patches_correct_path(self, invoices, mock_http):
        mock_http.patch.return_value = make_response(200, {**INVOICE_DATA, "status": "canceled"})
        invoices.cancel("guid-abc")
        assert mock_http.patch.call_args[0][0] == f"{BASE_HOST}/v1/invoices/guid-abc/cancel"


class TestAsyncInvoicesCreate:
    async def test_accepts_dict_delivery_value(self, settings):
        mock_http = MagicMock(spec=httpx.AsyncClient)
        mock_http.post = AsyncMock(return_value=make_response(201, INVOICE_DATA))
        resource = AsyncInvoicesResource(settings, mock_http, BASE_HOST)
        result = await resource.create(
            invoice_number="INV-001",
            amount=5000,
            description="Test",
            delivery_value={"email": "user@example.com"},
        )
        assert isinstance(result, Invoice)
        body = mock_http.post.call_args[1]["json"]
        assert body["delivery_value"] == {"email": "user@example.com"}
