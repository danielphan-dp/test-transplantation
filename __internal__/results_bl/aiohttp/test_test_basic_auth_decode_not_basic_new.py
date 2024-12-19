import pytest
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_empty_string() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("")

def test_basic_auth_decode_invalid_base64() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("InvalidBase64String")

def test_basic_auth_decode_partial_base64() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("dXNlcjoxMjM=")  # Assuming this is not a valid Basic Auth format

def test_basic_auth_decode_non_ascii() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic " + base64.b64encode("user:pass😊".encode('utf-8')).decode('utf-8'))