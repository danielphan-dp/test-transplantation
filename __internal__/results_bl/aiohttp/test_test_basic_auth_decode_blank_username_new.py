import base64
import pytest
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize('credentials, expected_auth', (
    (':', BasicAuth(login='', password='', encoding='utf-8')),
    ('username:', BasicAuth(login='username', password='', encoding='utf-8')),
    (':password', BasicAuth(login='', password='password', encoding='utf-8')),
    ('username:password', BasicAuth(login='username', password='password', encoding='utf-8')),
    ('invalid_base64', BasicAuth(login='', password='', encoding='utf-8')),  # Invalid base64
    ('', BasicAuth(login='', password='', encoding='utf-8')),  # Empty credentials
))
def test_basic_auth_decode_edge_cases(credentials: str, expected_auth: BasicAuth) -> None:
    header = f"Basic {base64.b64encode(credentials.encode()).decode()}" if credentials else "Basic "
    assert BasicAuth.decode(header) == expected_auth