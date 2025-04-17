import pytest
import aiohttp.helpers

@pytest.mark.parametrize("encoding, errors", [
    ("utf-8", "strict"),
    ("ascii", "ignore"),
    ("latin1", "replace"),
    ("utf-16", "strict"),
])
def test_basic_auth_decode_valid_encoding(encoding, errors):
    auth_header = "Basic " + aiohttp.helpers.encode_basic_auth_credentials("username", "password")
    result = aiohttp.helpers.BasicAuth.decode(auth_header, encoding=encoding)
    assert result.login == "username"
    assert result.password == "password"
    assert result.encoding == encoding

def test_basic_auth_decode_invalid_base64():
    with pytest.raises(ValueError):
        aiohttp.helpers.BasicAuth.decode("Basic InvalidBase64")

def test_basic_auth_decode_missing_auth_type():
    with pytest.raises(ValueError):
        aiohttp.helpers.BasicAuth.decode("InvalidHeader")

def test_basic_auth_decode_invalid_format():
    with pytest.raises(ValueError):
        aiohttp.helpers.BasicAuth.decode("Basic dXNlcm5hbWU6")  # valid base64 but missing password

def test_basic_auth_decode_none_login():
    with pytest.raises(ValueError):
        aiohttp.helpers.BasicAuth.decode("Basic " + aiohttp.helpers.encode_basic_auth_credentials(None, "password"))

def test_basic_auth_decode_none_password():
    with pytest.raises(ValueError):
        aiohttp.helpers.BasicAuth.decode("Basic " + aiohttp.helpers.encode_basic_auth_credentials("username", None))