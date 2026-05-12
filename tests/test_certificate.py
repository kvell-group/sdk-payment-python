from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from sdk_payment_python.models.certificate import CertificatePdf, CertificateTask
from sdk_payment_python.resources.payouts.certificate import AsyncPayoutCertificateResource, PayoutCertificateResource
from tests.conftest import BASE_HOST, make_response

TASK_DATA = {"task_id": "task-123", "status": "processing", "url": None}
PDF_DATA = {"file_url": "https://example.com/cert.pdf"}


@pytest.fixture
def certificate(settings, mock_http):
    return PayoutCertificateResource(settings, mock_http, BASE_HOST)


class TestCertificateSendEmail:
    def test_posts_to_correct_path(self, certificate, mock_http):
        mock_http.post.return_value = make_response(200, {})
        certificate.send_email("tx-123", "user@example.com")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123/operation-certificate"

    def test_body_has_email(self, certificate, mock_http):
        mock_http.post.return_value = make_response(200, {})
        certificate.send_email("tx-123", "user@example.com")
        body = mock_http.post.call_args[1]["json"]
        assert body["email"] == "user@example.com"

    def test_uses_sha256_signature(self, certificate, mock_http):
        mock_http.post.return_value = make_response(200, {})
        certificate.send_email("tx-123", "user@example.com")
        headers = mock_http.post.call_args[1]["headers"]
        assert "X-Signature" in headers

    def test_does_not_raise_on_empty_body(self, certificate, mock_http):
        mock_http.post.return_value = make_response(202)
        certificate.send_email("tx-123", "user@example.com")

    async def test_async_does_not_raise_on_empty_body(self, settings):
        mock_http = MagicMock(spec=httpx.AsyncClient)
        mock_http.post = AsyncMock(return_value=make_response(202))
        resource = AsyncPayoutCertificateResource(settings, mock_http, BASE_HOST)
        await resource.send_email("tx-123", "user@example.com")


class TestCertificateCreateView:
    def test_returns_certificate_task(self, certificate, mock_http):
        mock_http.post.return_value = make_response(200, TASK_DATA)
        result = certificate.create_view("tx-123")
        assert isinstance(result, CertificateTask)
        assert result.task_id == "task-123"

    def test_posts_to_correct_path(self, certificate, mock_http):
        mock_http.post.return_value = make_response(200, TASK_DATA)
        certificate.create_view("tx-123")
        assert mock_http.post.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123/operation-certificate/view"


class TestCertificateGetView:
    def test_returns_certificate_task(self, certificate, mock_http):
        mock_http.get.return_value = make_response(200, {**TASK_DATA, "status": "completed"})
        result = certificate.get_view("tx-123", "task-123")
        assert isinstance(result, CertificateTask)
        assert result.status == "completed"

    def test_gets_correct_path_with_params(self, certificate, mock_http):
        mock_http.get.return_value = make_response(200, TASK_DATA)
        certificate.get_view("tx-123", "task-123")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123/operation-certificate/view"
        params = mock_http.get.call_args[1]["params"]
        assert params["task_id"] == "task-123"


class TestCertificatePdf:
    def test_returns_certificate_pdf(self, certificate, mock_http):
        mock_http.get.return_value = make_response(200, PDF_DATA)
        result = certificate.pdf("tx-123")
        assert isinstance(result, CertificatePdf)
        assert result.file_url == "https://example.com/cert.pdf"

    def test_gets_correct_path(self, certificate, mock_http):
        mock_http.get.return_value = make_response(200, PDF_DATA)
        certificate.pdf("tx-123")
        assert mock_http.get.call_args[0][0] == f"{BASE_HOST}/v1/orders/tx-123/operation-certificate/pdf"
