import pytest
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize('header', [
    'Basic bmtpbTpwd2Q=',
    'basic bmtpbTpwd2Q=',
    'Basic bmtpbTpwd2Q==',  # Invalid base64
    'Basic ',               # Missing credentials
    'Basic bmtpbTpwd2Q=extra',  # Extra data
    'InvalidHeaderFormat'   # Completely invalid format
])
def test_basic_auth_decode(header: str) -> None:
    if header in ['Basic bmtpbTpwd2Q=', 'basic bmtpbTpwd2Q=']:
        auth = BasicAuth.decode(header)
        assert auth.login == "nkim"
        assert auth.password == "pwd"
    else:
        with pytest.raises(Exception):
            BasicAuth.decode(header)