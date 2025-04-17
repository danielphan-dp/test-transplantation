import pytest
from aiohttp import web
from multidict import CIMultiDict
from aiohttp import hdrs
from aiohttp.helpers import BasicAuth

@pytest.mark.parametrize(
    ('headers', 'expected_auth'),
    [
        (None, BasicAuth('username', 'pass')),
        (CIMultiDict({'Authorization': 'Basic dGhlIHNhbXBsZSBub25jZQ=='}), BasicAuth('username', 'pass')),
        (CIMultiDict({'Authorization': 'Bearer token'}), None),
    ]
)
def test_auth_header_handling(make_request, headers, expected_auth):
    """Test handling of different Authorization headers."""
    req = make_request("get", "http://example.com", headers=headers)
    if expected_auth:
        assert req.headers[hdrs.AUTHORIZATION] == expected_auth.encode()
    else:
        assert hdrs.AUTHORIZATION not in req.headers

def test_missing_host_header(make_request):
    """Test behavior when HOST header is missing."""
    req = make_request("get", "http://example.com", headers=CIMultiDict({'UPGRADE': 'websocket'}))
    assert req.headers[hdrs.HOST] == 'server.example.com'

def test_websocket_protocols_header(make_request):
    """Test inclusion of SEC-WEBSOCKET-PROTOCOL header when protocols are specified."""
    req = make_request("get", "http://example.com", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_default_headers(make_request):
    """Test that default headers are set correctly."""
    req = make_request("get", "http://example.com")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['ORIGIN'] == 'http://example.com'
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'