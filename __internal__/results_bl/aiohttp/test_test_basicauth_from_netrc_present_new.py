import pytest
from aiohttp import web, hdrs
from multidict import CIMultiDict
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize(('method', 'path', 'headers', 'expected_auth'), [
    ('get', 'http://example.com', None, BasicAuth('username', 'pass')),
    ('post', 'http://example.com', CIMultiDict({'AUTHORIZATION': 'Basic dXNlbmFtZTpwYXNz'}), BasicAuth('username', 'pass')),
    ('put', 'http://example.com', CIMultiDict({'AUTHORIZATION': 'Basic dXNlbmFtZTpwYXNz'}), BasicAuth('username', 'pass')),
    ('delete', 'http://example.com', CIMultiDict({'AUTHORIZATION': 'Basic dXNlbmFtZTpwYXNz'}), BasicAuth('username', 'pass')),
])
@pytest.mark.usefixtures('netrc_contents')
def test_basicauth_with_various_methods(make_request, method, path, headers, expected_auth):
    """Test Authorization header with various HTTP methods and headers."""
    req = make_request(method, path, headers=headers)
    assert req.headers[hdrs.AUTHORIZATION] == expected_auth.encode()

@pytest.mark.parametrize(('method', 'path', 'headers'), [
    ('get', 'http://example.com', CIMultiDict({'HOST': 'server.example.com'})),
    ('post', 'http://example.com', CIMultiDict({'UPGRADE': 'websocket'})),
])
@pytest.mark.usefixtures('netrc_contents')
def test_basicauth_no_auth_header(make_request, method, path, headers):
    """Test behavior when no Authorization header is provided."""
    req = make_request(method, path, headers=headers)
    assert hdrs.AUTHORIZATION not in req.headers

@pytest.mark.parametrize(('method', 'path', 'protocols', 'expected_protocol'), [
    ('get', 'http://example.com', True, 'chat, superchat'),
    ('post', 'http://example.com', False, None),
])
@pytest.mark.usefixtures('netrc_contents')
def test_basicauth_with_protocols(make_request, method, path, protocols, expected_protocol):
    """Test Authorization header with protocols specified."""
    req = make_request(method, path, protocols=protocols)
    if expected_protocol:
        assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == expected_protocol
    else:
        assert 'SEC-WEBSOCKET-PROTOCOL' not in req.headers