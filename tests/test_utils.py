import hashlib

from sdk_payment_python.utils import KvellUtils


def _sha256(*parts: str) -> str:
    return hashlib.sha256("".join(parts).encode()).hexdigest()


class TestCreateSignature:
    def test_basic(self):
        result = KvellUtils.create_signature("api", "secret", ["tx1", 1000])
        assert result == _sha256("api", "tx1", "1000", "secret")

    def test_single_value(self):
        result = KvellUtils.create_signature("api", "secret", ["tx1"])
        assert result == _sha256("api", "tx1", "secret")

    def test_different_inputs_produce_different_signatures(self):
        sig1 = KvellUtils.create_signature("api", "secret", ["tx1", 1000])
        sig2 = KvellUtils.create_signature("api", "secret", ["tx2", 1000])
        assert sig1 != sig2

    def test_values_order_matters(self):
        sig1 = KvellUtils.create_signature("api", "secret", ["tx1", 1000])
        sig2 = KvellUtils.create_signature("api", "secret", [1000, "tx1"])
        assert sig1 != sig2


class TestCreateSignatureByJsonBody:
    def test_basic(self):
        result = KvellUtils.create_signature_by_json_body("api", "secret", {"key": "val"})
        assert result == _sha256("api", '{"key":"val"}', "secret")

    def test_key_order_preserved(self):
        sig1 = KvellUtils.create_signature_by_json_body("api", "secret", {"a": 1, "b": 2})
        sig2 = KvellUtils.create_signature_by_json_body("api", "secret", {"b": 2, "a": 1})
        assert sig1 != sig2
