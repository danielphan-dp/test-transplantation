import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_port_default_http(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com/")
    assert req.host == "example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_port_default_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://example.com/")
    assert req.host == "example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://example.com/", headers=headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://example.com/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_host_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")