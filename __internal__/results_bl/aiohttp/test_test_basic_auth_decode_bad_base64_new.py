import pytest
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_empty_string() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("")

def test_basic_auth_decode_invalid_encoding() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic bmtpbTpwd2Q", encoding='invalid-encoding')

def test_basic_auth_decode_missing_prefix() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("bmtpbTpwd2Q")

def test_basic_auth_decode_non_base64_string() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic non_base64_string")

def test_basic_auth_decode_valid_base64() -> None:
    result = BasicAuth.decode("Basic YWRtaW46cGFzc3dvcmQ=")
    assert result == "admin:password"