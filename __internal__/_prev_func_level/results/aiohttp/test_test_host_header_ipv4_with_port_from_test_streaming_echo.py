import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_header_ipv4_without_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://127.0.0.2")
    assert req.headers["HOST"] == "127.0.0.2"

def test_host_header_ipv6_with_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://[::1]:99")
    assert req.headers["HOST"] == "[::1]:99"

def test_host_header_ipv6_without_port(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://[::1]")
    assert req.headers["HOST"] == "[::1]"

def test_host_header_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "http://127.0.0.2", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://127.0.0.2", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"