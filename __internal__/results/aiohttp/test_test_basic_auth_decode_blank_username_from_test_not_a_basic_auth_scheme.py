import base64
import pytest
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize("credentials, expected_auth", [
    (':', BasicAuth(login='', password='', encoding='latin1')),
    ('username:', BasicAuth(login='username', password='', encoding='latin1')),
    (':password', BasicAuth(login='', password='password', encoding='latin1')),
    ('username:password', BasicAuth(login='username', password='password', encoding='latin1')),
    ('invalid_format', None),  # Testing invalid format
    ('Basic ', None),  # Testing empty credentials
    ('Basic ' + base64.b64encode(b'username:').decode(), BasicAuth(login='username', password='', encoding='latin1')),  # Testing username only
    ('Basic ' + base64.b64encode(b':password').decode(), BasicAuth(login='', password='password', encoding='latin1')),  # Testing password only
])
def test_basic_auth_decode(credentials, expected_auth):
    if expected_auth is None:
        with pytest.raises(ValueError):
            BasicAuth.decode(f"Basic {credentials}")
    else:
        assert BasicAuth.decode(f"Basic {base64.b64encode(credentials.encode()).decode()}") == expected_auth