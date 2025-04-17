import pytest
import base64
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize("header, expected_username, expected_password", [
    ("Basic " + base64.b64encode(b"username:password").decode(), "username", "password"),
    ("Basic " + base64.b64encode(b"testuser:testpass").decode(), "testuser", "testpass"),
])
def test_basic_auth_decode_valid_credentials(header, expected_username, expected_password):
    auth = BasicAuth.decode(header)
    assert auth.login == expected_username
    assert auth.password == expected_password

def test_basic_auth_decode_invalid_format():
    with pytest.raises(ValueError, match="Could not parse authorization header."):
        BasicAuth.decode("InvalidHeader")

def test_basic_auth_decode_missing_credentials():
    with pytest.raises(ValueError, match="Invalid credentials."):
        BasicAuth.decode("Basic ")

def test_basic_auth_decode_invalid_base64():
    with pytest.raises(ValueError, match="Invalid base64 encoding."):
        BasicAuth.decode("Basic InvalidBase64")

def test_basic_auth_decode_invalid_auth_type():
    with pytest.raises(ValueError, match="Unknown authorization method"):
        BasicAuth.decode("Bearer " + base64.b64encode(b"username:password").decode())