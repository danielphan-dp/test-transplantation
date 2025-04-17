import pytest
import base64
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize("auth_header, expected_username, expected_password", [
    ("Basic " + base64.b64encode(b"username:password").decode('ascii'), "username", "password"),
    ("Basic " + base64.b64encode(b"user:pass").decode('ascii'), "user", "pass"),
])
def test_basic_auth_decode_valid(auth_header, expected_username, expected_password):
    auth = BasicAuth.decode(auth_header)
    assert auth.login == expected_username
    assert auth.password == expected_password

def test_basic_auth_decode_invalid_format():
    with pytest.raises(ValueError):
        BasicAuth.decode("InvalidHeader")

def test_basic_auth_decode_missing_credentials():
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic ")

def test_basic_auth_decode_bad_base64():
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic bmtpbTpwd2Q")