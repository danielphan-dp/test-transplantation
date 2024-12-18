import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "/path", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/path")

def test_make_request_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    assert req.path == "/"  # Assuming the default behavior is to normalize to root path

def test_make_request_with_ssl(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://example.com/")
    assert req.is_ssl() is True

def test_make_request_with_ipv6_address(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://[2001:db8::1]/")
    assert req.host == "2001:db8::1"
    assert req.port == 443
    assert req.is_ssl()