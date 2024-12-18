import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_port_custom_http(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com:8080/")
    assert req.host == "example.com"
    assert req.port == 8080
    assert not req.is_ssl()

def test_host_port_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'custom.example.com', 'X-Custom-Header': 'value'})
    req = make_request("get", "/", headers=headers)
    assert req.host == "custom.example.com"
    assert req.headers['X-Custom-Header'] == 'value'

def test_host_with_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")

def test_host_with_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")
    assert req.headers['HOST'] == 'server.example.com'
    assert 'SEC-WEBSOCKET-KEY' in req.headers

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'