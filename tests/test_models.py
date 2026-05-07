from sdk_payment_python.models.invoice import Invoice
from sdk_payment_python.models.qr import QRTemplate
from sdk_payment_python.models.session import AlfaPayResult, SessionCreated, SbpResult
from sdk_payment_python.models.transaction import Transaction


class TestFromDict:
    def test_unknown_fields_are_ignored(self):
        invoice = Invoice.from_dict(
            {
                "invoice_guid": "abc",
                "status": "new",
                "amount": 1000,
                "url": "https://pay",
                "created_at": "2024-01-01",
                "expired_at": "2024-01-02",
                "unknown_field": "should_be_ignored",
            }
        )
        assert not hasattr(invoice, "unknown_field")

    def test_optional_fields_default_to_none(self):
        invoice = Invoice.from_dict(
            {
                "invoice_guid": "abc",
                "status": "new",
                "amount": 1000,
                "url": "https://pay",
                "created_at": "2024-01-01",
                "expired_at": "2024-01-02",
            }
        )
        assert invoice.description is None
        assert invoice.delivery_type is None

    def test_optional_fields_populated(self):
        invoice = Invoice.from_dict(
            {
                "invoice_guid": "abc",
                "status": "new",
                "amount": 1000,
                "url": "https://pay",
                "created_at": "2024-01-01",
                "expired_at": "2024-01-02",
                "description": "Test",
                "delivery_type": "sms",
            }
        )
        assert invoice.description == "Test"
        assert invoice.delivery_type == "sms"


class TestSessionModels:
    def test_session_created(self):
        result = SessionCreated.from_dict({"ok": True, "extra": "ignored"})
        assert result.ok is True

    def test_sbp_result(self):
        result = SbpResult.from_dict({"form_url": "https://sbp.link"})
        assert result.form_url == "https://sbp.link"

    def test_alfapay_result(self):
        result = AlfaPayResult.from_dict({"form_url": "https://alfa.link"})
        assert result.form_url == "https://alfa.link"


class TestTransactionModel:
    def test_required_fields(self):
        tx = Transaction.from_dict(
            {
                "id": 1,
                "status": "completed",
                "amount": 5000,
                "transaction": "tx-123",
                "description": "Test",
                "created_at": "2024-01-01",
            }
        )
        assert tx.id == 1
        assert tx.status == "completed"
        assert tx.commission is None

    def test_optional_fields(self):
        tx = Transaction.from_dict(
            {
                "id": 1,
                "status": "completed",
                "amount": 5000,
                "transaction": "tx-123",
                "description": "Test",
                "created_at": "2024-01-01",
                "commission": 150,
                "instrument": "sbp",
            }
        )
        assert tx.commission == 150
        assert tx.instrument == "sbp"


class TestQRTemplateModel:
    def test_from_dict(self):
        qr = QRTemplate.from_dict(
            {
                "id": "qr-1",
                "name": "My QR",
                "payment_purpose": "Payment",
                "qr_payload": "https://nspk.ru/...",
                "qr_image": "base64==",
                "currency": "RUB",
                "amount": 1000,
            }
        )
        assert qr.id == "qr-1"
        assert qr.amount == 1000
        assert qr.start_date is None
