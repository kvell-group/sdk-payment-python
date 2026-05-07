import base64
import hashlib
import json
import logging
import typing

from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15

logger = logging.getLogger(__name__)


class KvellUtils:
    @classmethod
    def create_signature(cls, api_key: str, secret_key: str, values: typing.Iterable[typing.Any]) -> str:
        values = [
            str(api_key),
            *list(map(str, values)),
            str(secret_key),
        ]
        pre_sign = "".join(values)
        logger.debug("KVELL pre_sign: %s", pre_sign)
        return hashlib.sha256(pre_sign.encode()).hexdigest()

    @classmethod
    def create_signature_by_json_body(cls, api_key: str, secret_key: str, values: dict) -> str:
        values = [
            str(api_key),
            json.dumps(values, separators=(",", ":"), ensure_ascii=False),
            str(secret_key),
        ]
        pre_sign = "".join(values)
        logger.debug("KVELL pre_sign: %s", pre_sign)
        return hashlib.sha256(pre_sign.encode()).hexdigest()

    @classmethod
    def create_rsa_signature(cls, private_key: str, body: dict) -> str:
        body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)
        key = RSA.import_key(private_key)
        h = SHA256.new(body_str.encode())
        signature = pkcs1_15.new(key).sign(h)
        return base64.b64encode(signature).decode()

    @classmethod
    def verify_callback_signature(cls, api_key: str, raw_body: str, secret_key: str, signature: str) -> bool:
        expected = hashlib.sha256((api_key + raw_body + secret_key).encode()).hexdigest()
        return expected == signature
