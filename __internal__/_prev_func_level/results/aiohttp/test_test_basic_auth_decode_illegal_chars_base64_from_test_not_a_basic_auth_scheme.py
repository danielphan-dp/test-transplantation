import pytest
import base64
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize('header', [
    'Basic dXNlcm5hbWU6cGFzc3dvcmQ=',  # valid base64
    'Basic dXNlcm5hbWU6',               # valid base64 with missing password
    'Basic dXNlcm5hbWU6cGFzc3dvcmQ',    # invalid base64 (missing padding)
    'Basic dXNlcm5hbWU6cGFzc3dvcmQ==',  # valid base64 with padding
    'Basic ???',                         # invalid base64
    'Basic   ',                          # invalid base64 (empty credentials)
])
def test_basic_auth_decode(header: str) -> None:
    if header in ['Basic ???', 'Basic   ', 'Basic dXNlcm5hbWU6']:
        with pytest.raises(ValueError, match="Invalid base64 encoding."):
            BasicAuth.decode(header)
    else:
        result = BasicAuth.decode(header)
        assert isinstance(result, BasicAuth)