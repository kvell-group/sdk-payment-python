from __future__ import annotations

import hashlib

from sdk_payment_python.utils import KvellUtils


class TestVerifyCallbackSignature:
    def _make_sig(self, api_key: str, body: str, secret_key: str) -> str:
        return hashlib.sha256((api_key + body + secret_key).encode()).hexdigest()

    def test_valid_signature_returns_true(self):
        api_key, secret_key = "key", "secret"
        body = '{"event":"payment","transaction":"tx-1"}'
        sig = self._make_sig(api_key, body, secret_key)
        assert KvellUtils.verify_callback_signature(api_key, body, secret_key, sig) is True

    def test_invalid_signature_returns_false(self):
        assert KvellUtils.verify_callback_signature("key", "body", "secret", "wrong-sig") is False

    def test_tampered_body_returns_false(self):
        api_key, secret_key = "key", "secret"
        original_body = '{"amount":1000}'
        tampered_body = '{"amount":9999}'
        sig = self._make_sig(api_key, original_body, secret_key)
        assert KvellUtils.verify_callback_signature(api_key, tampered_body, secret_key, sig) is False

    def test_empty_body_handled(self):
        api_key, secret_key = "key", "secret"
        sig = self._make_sig(api_key, "", secret_key)
        assert KvellUtils.verify_callback_signature(api_key, "", secret_key, sig) is True
