import pytest
import base64
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_empty_header() -> None:
    with pytest.raises(ValueError, match="Invalid credentials."):
        header = "Basic {}".format(base64.b64encode(b"").decode())
        BasicAuth.decode(header)

def test_basic_auth_decode_invalid_encoding() -> None:
    with pytest.raises(ValueError, match="Invalid credentials."):
        header = "Basic {}".format(base64.b64encode(b"username:password").decode('latin1'))
        BasicAuth.decode(header)

def test_basic_auth_decode_missing_colon() -> None:
    with pytest.raises(ValueError, match="Invalid credentials."):
        header = "Basic {}".format(base64.b64encode(b"usernamepassword").decode())
        BasicAuth.decode(header)

def test_basic_auth_decode_extra_colon() -> None:
    with pytest.raises(ValueError, match="Invalid credentials."):
        header = "Basic {}".format(base64.b64encode(b"username:password:extra").decode())
        BasicAuth.decode(header)

def test_basic_auth_decode_valid_credentials() -> None:
    header = "Basic {}".format(base64.b64encode(b"username:password").decode())
    assert BasicAuth.decode(header) == "username:password"