import pytest
import base64
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_valid_credentials() -> None:
    header = "Basic {}".format(base64.b64encode(b"username:password").decode())
    auth = BasicAuth.decode(header)
    assert auth.login == "username"
    assert auth.password == "password"

def test_basic_auth_decode_invalid_base64() -> None:
    header = "Basic invalid_base64"
    with pytest.raises(ValueError, match="Invalid base64 encoding."):
        BasicAuth.decode(header)

def test_basic_auth_decode_missing_credentials() -> None:
    header = "Basic "
    with pytest.raises(ValueError, match="Could not parse authorization header."):
        BasicAuth.decode(header)

def test_basic_auth_decode_not_basic_scheme() -> None:
    header = "Bearer {}".format(base64.b64encode(b"username:password").decode())
    with pytest.raises(ValueError, match="Unknown authorization method Bearer"):
        BasicAuth.decode(header)

def test_basic_auth_decode_invalid_credentials_format() -> None:
    header = "Basic {}".format(base64.b64encode(b"username").decode())
    with pytest.raises(ValueError, match="Invalid credentials."):
        BasicAuth.decode(header)