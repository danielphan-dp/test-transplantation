import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert "UPGRADE" in req.headers
    assert req.headers["UPGRADE"] == "websocket"

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {"user-agent": "my custom agent", "x-custom-header": "custom value"}
    req = make_request("get", "/", headers=custom_headers)
    assert "USER-Agent" in req.headers
    assert req.headers["User-Agent"] == "my custom agent"
    assert "X-Custom-Header" in req.headers
    assert req.headers["X-Custom-Header"] == "custom value"

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")
    assert "SEC-WEBSOCKET-KEY" in req.headers
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="

def test_make_request_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/")