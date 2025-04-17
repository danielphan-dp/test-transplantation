import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_header_default(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {"host": "custom.example.com"}
    req = make_request("get", "http://python.org/", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"

def test_host_header_with_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={})
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_header_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org/")