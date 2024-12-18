import pytest
import base64
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize("header, expected_login, expected_password", [
    ('Basic bmtpbTpwd2Q=', 'nkim', 'pwd'),
    ('Basic bmtpbTpwd=', 'nkim', ''),
    ('Basic bmtpbTpwd2Q==', 'nkim', 'pwd'),  # Invalid base64, should raise error
    ('Basic ', None, None),  # Missing credentials
    ('InvalidScheme bmtpbTpwd2Q=', None, None),  # Invalid scheme
])
def test_basic_auth_decode(header, expected_login, expected_password):
    if expected_login is None and expected_password is None:
        with pytest.raises(ValueError):
            BasicAuth.decode(header)
    else:
        auth = BasicAuth.decode(header)
        assert auth.login == expected_login
        assert auth.password == expected_password

def test_basic_auth_decode_invalid_base64():
    with pytest.raises(ValueError):
        BasicAuth.decode('Basic invalid_base64==')