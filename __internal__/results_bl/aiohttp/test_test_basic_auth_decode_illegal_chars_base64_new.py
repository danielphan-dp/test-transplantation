import pytest
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize('header', [
    'Basic ???',
    'Basic   ',
    'Basic YWJjMTIz',  # valid base64
    'Basic YWJjMTIz==',  # invalid padding
    'Basic YWJjMTIz@#$',  # invalid characters
    'Basic ' + 'A' * 1000,  # long string
])
def test_basic_auth_decode_edge_cases(header: str) -> None:
    if header in ['Basic ???', 'Basic   ', 'Basic YWJjMTIz@#$']:
        with pytest.raises(ValueError, match="Invalid base64 encoding."):
            BasicAuth.decode(header)
    elif header == 'Basic YWJjMTIz==':
        with pytest.raises(ValueError, match="Invalid base64 encoding."):
            BasicAuth.decode(header)
    else:
        assert BasicAuth.decode(header) == 'abc123'  # expected output for valid base64