import pytest
import base64
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize('header, expected_login, expected_password', [
    ('Basic bmtpbTpwd2Q=', 'nkim', 'pwd'),
    ('basic bmtpbTpwd2Q=', 'nkim', 'pwd'),
    ('Basic ' + base64.b64encode(b'nkim:pwd').decode('ascii'), 'nkim', 'pwd'),
    ('Basic ' + base64.b64encode(b'username:password').decode('ascii'), 'username', 'password'),
    ('Basic ' + base64.b64encode(b'foo:bar').decode('ascii'), 'foo', 'bar'),
])
def test_basic_auth_decode(header, expected_login, expected_password):
    auth = BasicAuth.decode(header)
    assert auth.login == expected_login
    assert auth.password == expected_password

@pytest.mark.parametrize('header', [
    'Bearer token',
    'Digest username="nkim", realm="test", nonce="abc", uri="/", response="xyz"',
    'InvalidHeaderFormat'
])
def test_basic_auth_decode_invalid(header):
    with pytest.raises(ValueError):
        BasicAuth.decode(header)