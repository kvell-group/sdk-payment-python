from __future__ import annotations

from unittest.mock import MagicMock

import httpx
import pytest

from sdk_payment_python.settings import KvellSettings

API_KEY = "test_api_key"
SECRET_KEY = "test_secret_key"
BASE_HOST = "http://api.pay.kvell.group"
CHECKOUT_HOST = "https://pay.kvell.group"


@pytest.fixture
def settings():
    return KvellSettings(api_key=API_KEY, secret_key=SECRET_KEY)


def make_response(status_code: int = 200, json_data: dict | None = None) -> MagicMock:
    response = MagicMock(spec=httpx.Response)
    response.status_code = status_code
    response.is_error = status_code >= 400
    response.json.return_value = json_data or {}
    response.text = str(json_data)
    response.content = b"" if json_data is None else b"{}"
    return response


@pytest.fixture
def mock_http():
    return MagicMock(spec=httpx.Client)
