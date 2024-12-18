import pytest
from aiohttp import web, hdrs
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_no_authorization_header_when_trust_env_false(make_request: _RequestMaker) -> None:
    """Test no authorization header is sent via netrc if trust_env is False"""
    req = make_request("get", "http://example.com", trust_env=False)
    assert hdrs.AUTHORIZATION not in req.headers

def test_authorization_header_present_when_trust_env_true(make_request: _RequestMaker) -> None:
    """Test authorization header is sent via netrc if trust_env is True"""
    req = make_request("get", "http://example.com", trust_env=True)
    assert hdrs.AUTHORIZATION in req.headers

def test_custom_headers_in_request(make_request: _RequestMaker) -> None:
    """Test custom headers are included in the request"""
    custom_headers = CIMultiDict({'X-Custom-Header': 'value'})
    req = make_request("get", "http://example.com", headers=custom_headers)
    assert req.headers['X-Custom-Header'] == 'value'

def test_protocols_in_request(make_request: _RequestMaker) -> None:
    """Test protocols are included in the request headers"""
    req = make_request("get", "http://example.com", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_default_headers_in_request(make_request: _RequestMaker) -> None:
    """Test default headers are included in the request"""
    req = make_request("get", "http://example.com")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['ORIGIN'] == 'http://example.com'
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'