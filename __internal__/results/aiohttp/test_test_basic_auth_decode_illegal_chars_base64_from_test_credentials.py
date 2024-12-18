import pytest
import aiohttp.helpers

@pytest.mark.parametrize('encoding', ['utf-8', 'ascii', 'latin1', 'invalid-encoding'])
def test_basic_auth_decode_edge_cases(encoding):
    if encoding == 'invalid-encoding':
        with pytest.raises(LookupError, match="unknown encoding: invalid-encoding"):
            aiohttp.helpers.BasicAuth.decode('Basic dXNlcm5hbWU6cGFzc3dvcmQ=', encoding=encoding)
    else:
        decoded = aiohttp.helpers.BasicAuth.decode('Basic dXNlcm5hbWU6cGFzc3dvcmQ=', encoding=encoding)
        assert decoded == 'username:password'