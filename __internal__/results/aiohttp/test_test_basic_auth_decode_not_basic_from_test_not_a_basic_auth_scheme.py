import pytest
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_invalid_format() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("InvalidFormat")

def test_basic_auth_decode_missing_credentials() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic ")

def test_basic_auth_decode_invalid_base64() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic InvalidBase64==")

def test_basic_auth_decode_non_basic_scheme() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Bearer dGVzdDoxMjM0NTY3OA==")

def test_basic_auth_decode_valid_credentials() -> None:
    auth = BasicAuth.decode("Basic Y2hhcmxlczpwYXNzd29yZA==")
    assert auth.login == "charles"
    assert auth.password == "password"