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

def test_basic_auth_decode_missing_colon() -> None:
    header = "Basic {}".format(base64.b64encode(b"usernamepassword").decode())
    with pytest.raises(ValueError, match="Invalid credentials."):
        BasicAuth.decode(header)

def test_basic_auth_decode_no_auth_type() -> None:
    header = "NoAuth {}".format(base64.b64encode(b"username:password").decode())
    with pytest.raises(ValueError, match="Unknown authorization method NoAuth"):
        BasicAuth.decode(header)

def test_basic_auth_decode_empty_header() -> None:
    header = ""
    with pytest.raises(ValueError, match="Could not parse authorization header."):
        BasicAuth.decode(header)

def test_basic_auth_decode_none_login() -> None:
    with pytest.raises(ValueError, match="None is not allowed as login value"):
        BasicAuth(None, "password")

def test_basic_auth_decode_none_password() -> None:
    with pytest.raises(ValueError, match="None is not allowed as password value"):
        BasicAuth("username", None)

def test_basic_auth_decode_invalid_login_character() -> None:
    with pytest.raises(ValueError, match='A ":" is not allowed in login'):
        BasicAuth("user:name", "password")