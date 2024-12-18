import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_header_host_empty(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://")
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_host_invalid(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://invalid_host")
    assert req.headers["HOST"] == "invalid_host"

def test_host_header_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_header_host_unicode_edge_case(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://éé.com")
    assert req.headers["HOST"] == "xn--9caa.com"

def test_host_header_host_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "http://example.com", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"