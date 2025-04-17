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

def test_host_port_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_port_nondefault_https(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://secure.example.com:8443/")
    assert req.host == "secure.example.com"
    assert req.port == 8443
    assert req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://custom.example.com/", headers=headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'
    assert req.host == "custom.example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://protocols.example.com/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'
    assert req.host == "protocols.example.com"
    assert req.port == 80
    assert not req.is_ssl()