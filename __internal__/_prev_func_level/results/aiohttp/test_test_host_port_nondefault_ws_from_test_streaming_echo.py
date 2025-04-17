import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_port_default_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://localhost/")
    assert req.host == "localhost"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_port_ssl_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://secure.example.com:443/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "ws://custom.example.com/", headers=headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'
    assert req.host == "custom.example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://protocols.example.com/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'
    assert req.host == "protocols.example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_invalid_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://invalid.port:99999/")
    assert req.host == "invalid.port"
    assert req.port == 99999
    assert not req.is_ssl()