import pytest
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_empty_header() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("")

def test_basic_auth_decode_invalid_scheme() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("InvalidScheme dGVzdDpwYXNzd29yZA==")

def test_basic_auth_decode_invalid_base64() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic bmtpbTpwd2Q")

def test_basic_auth_decode_missing_colon() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic " + base64.b64encode(b"usernamewithoutcolon").decode('ascii'))

def test_basic_auth_decode_valid_credentials() -> None:
    auth = BasicAuth.decode("Basic " + base64.b64encode(b"username:password").decode('ascii'))
    assert auth.login == "username"
    assert auth.password == "password"
    assert auth.encoding == "latin1"  # default encoding

def test_basic_auth_decode_invalid_base64_with_padding() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic bmtpbTpwd2Q==")  # Invalid base64 padding

def test_basic_auth_decode_none_login() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic " + base64.b64encode(b":password").decode('ascii'))

def test_basic_auth_decode_none_password() -> None:
    auth = BasicAuth.decode("Basic " + base64.b64encode(b"username:").decode('ascii'))
    assert auth.login == "username"
    assert auth.password == ""