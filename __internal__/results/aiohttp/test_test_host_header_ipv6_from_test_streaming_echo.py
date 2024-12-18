import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_header_with_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_with_custom_host(make_request: _RequestMaker) -> None:
    custom_host = "custom.example.com"
    req = make_request("get", "/", headers=CIMultiDict({'HOST': custom_host}))
    assert req.headers["HOST"] == custom_host

def test_host_header_with_ipv4(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://192.168.1.1")
    assert req.headers["HOST"] == "192.168.1.1"

def test_host_header_with_empty_host(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", headers=CIMultiDict({'HOST': ''}))
    assert req.headers["HOST"] == ''

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == 'chat, superchat'