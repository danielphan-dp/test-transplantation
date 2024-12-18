import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_headers_with_default_values(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com/")
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert "UPGRADE" in req.headers
    assert req.headers["UPGRADE"] == "websocket"
    assert "CONNECTION" in req.headers
    assert req.headers["CONNECTION"] == "Upgrade"
    assert "SEC-WEBSOCKET-KEY" in req.headers
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="
    assert "ORIGIN" in req.headers
    assert req.headers["ORIGIN"] == "http://example.com"
    assert "SEC-WEBSOCKET-VERSION" in req.headers
    assert req.headers["SEC-WEBSOCKET-VERSION"] == "13"

def test_headers_with_custom_values(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({"X-Custom-Header": "CustomValue"})
    req = make_request("post", "http://example.com/", headers=custom_headers)
    assert "X-CUSTOM-HEADER" in req.headers
    assert req.headers["X-CUSTOM-HEADER"] == "CustomValue"

def test_headers_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com/", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_missing_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com/", headers=None)
    assert "HOST" in req.headers
    assert "UPGRADE" in req.headers
    assert "CONNECTION" in req.headers
    assert "SEC-WEBSOCKET-KEY" in req.headers
    assert "ORIGIN" in req.headers
    assert "SEC-WEBSOCKET-VERSION" in req.headers

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "http://example.com/")