import pytest
from aiohttp import hdrs
from multidict import CIMultiDict

@pytest.mark.parametrize('headers, expected', [
    (None, False),
    (CIMultiDict({'Authorization': 'Bearer token'}), True),
    (CIMultiDict({'Authorization': 'Basic dXNlcm5hbWU6cGFzc3dvcmQ='}), True),
    (CIMultiDict({'Custom-Header': 'value'}), False),
])
def test_authorization_header(make_request, headers, expected) -> None:
    """Test that the Authorization header is sent or not based on input headers"""
    req = make_request("get", "http://example.com", headers=headers)
    assert (hdrs.AUTHORIZATION in req.headers) is expected

@pytest.mark.parametrize('protocols, expected_protocol', [
    (False, None),
    (True, 'chat, superchat'),
])
def test_websocket_protocols(make_request, protocols, expected_protocol) -> None:
    """Test that the SEC-WEBSOCKET-PROTOCOL header is set correctly based on protocols flag"""
    req = make_request("get", "http://example.com", protocols=protocols)
    if expected_protocol:
        assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == expected_protocol
    else:
        assert 'SEC-WEBSOCKET-PROTOCOL' not in req.headers

def test_default_headers(make_request) -> None:
    """Test that default headers are set correctly when no headers are provided"""
    req = make_request("get", "http://example.com")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['ORIGIN'] == 'http://example.com'
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'