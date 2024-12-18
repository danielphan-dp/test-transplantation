import pytest
import base64
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_invalid_auth_type() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Bearer token")

def test_basic_auth_decode_missing_credentials() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic ")

def test_basic_auth_decode_invalid_base64() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic invalid_base64")

def test_basic_auth_decode_valid_credentials() -> None:
    auth_header = "Basic " + base64.b64encode(b"username:password").decode("ascii")
    result = BasicAuth.decode(auth_header)
    assert result.login == "username"
    assert result.password == "password"
    assert result.encoding == "latin1"

def test_basic_auth_decode_invalid_character_in_login() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic " + base64.b64encode(b"user:name").decode("ascii"))