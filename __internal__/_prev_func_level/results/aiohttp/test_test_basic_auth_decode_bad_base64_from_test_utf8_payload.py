import pytest
import base64
from aiohttp.helpers import BasicAuth

def test_basic_auth_decode_valid_credentials() -> None:
    auth_header = 'Basic ' + base64.b64encode(b'username:password').decode('latin1')
    result = BasicAuth.decode(auth_header)
    assert result.login == 'username'
    assert result.password == 'password'
    assert result.encoding == 'latin1'

def test_basic_auth_decode_invalid_base64() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic invalid_base64")

def test_basic_auth_decode_missing_colon() -> None:
    auth_header = 'Basic ' + base64.b64encode(b'usernamepassword').decode('latin1')
    with pytest.raises(ValueError):
        BasicAuth.decode(auth_header)

def test_basic_auth_decode_empty_credentials() -> None:
    auth_header = 'Basic ' + base64.b64encode(b':').decode('latin1')
    result = BasicAuth.decode(auth_header)
    assert result.login == ''
    assert result.password == ''

def test_basic_auth_decode_none_login() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic " + base64.b64encode(b':password').decode('latin1'))

def test_basic_auth_decode_none_password() -> None:
    with pytest.raises(ValueError):
        BasicAuth.decode("Basic " + base64.b64encode(b'username:').decode('latin1'))