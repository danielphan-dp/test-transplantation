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
    req = make_request("get", "/test")
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

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({"CUSTOM-HEADER": "custom_value"})
    req = make_request("get", "/test", headers=custom_headers)
    assert "CUSTOM-HEADER" in req.headers
    assert req.headers["CUSTOM-HEADER"] == "custom_value"

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/test", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/test")