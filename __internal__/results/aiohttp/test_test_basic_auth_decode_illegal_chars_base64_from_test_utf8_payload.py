import pytest
import base64
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize('header', [
    'Basic ' + base64.b64encode(b'username:password').decode('latin-1'),
    'Basic ' + base64.b64encode(b'user:pass').decode('latin-1'),
    'Basic ' + base64.b64encode(b'').decode('latin-1'),
    'Basic ' + base64.b64encode(b'username:').decode('latin-1'),
    'Basic ' + base64.b64encode(b':password').decode('latin-1'),
])
def test_basic_auth_decode_valid_cases(header):
    auth = BasicAuth.decode(header)
    assert auth.login in ['username', 'user']
    assert auth.password in ['password', 'pass', '']

@pytest.mark.parametrize('header', [
    'Basic ???',
    'Basic   ',
    'Basic ' + base64.b64encode(b'username:password').decode('latin-1') + ' extra',
    'Bearer ' + base64.b64encode(b'username:password').decode('latin-1'),
])
def test_basic_auth_decode_illegal_chars_base64(header):
    with pytest.raises(ValueError, match="Invalid base64 encoding."):
        BasicAuth.decode(header)

@pytest.mark.parametrize('header', [
    'Basic ' + base64.b64encode(b'username:password').decode('latin-1'),
    'Basic ' + base64.b64encode(b'username:').decode('latin-1'),
    'Basic ' + base64.b64encode(b':password').decode('latin-1'),
])
def test_basic_auth_decode_edge_cases(header):
    auth = BasicAuth.decode(header)
    assert isinstance(auth, BasicAuth)