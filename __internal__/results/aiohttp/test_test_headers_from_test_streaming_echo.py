import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_with_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")

    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert "UPGRADE" in req.headers
    assert req.headers["UPGRADE"] == "websocket"
    assert "SEC-WEBSOCKET-KEY" in req.headers
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {"X-Custom-Header": "CustomValue"}
    req = make_request("post", "/test", headers=custom_headers)

    assert "X-Custom-Header" in req.headers
    assert req.headers["X-Custom-Header"] == "CustomValue"

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", protocols=True)

    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/")

def test_make_request_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")

    assert req.path == ""