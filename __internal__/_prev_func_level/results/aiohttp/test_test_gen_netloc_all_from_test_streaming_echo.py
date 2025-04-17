import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_default_headers(make_request: _RequestMaker, app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    req = make_request("get", "/test")
    assert req.headers["HOST"] == "server.example.com"
    assert req.headers["UPGRADE"] == "websocket"
    assert req.headers["CONNECTION"] == "Upgrade"
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="
    assert req.headers["ORIGIN"] == "http://example.com"
    assert req.headers["SEC-WEBSOCKET-VERSION"] == "13"

def test_make_request_with_protocols(make_request: _RequestMaker, app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    req = make_request("get", "/test", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_custom_headers(make_request: _RequestMaker, app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    custom_headers = CIMultiDict({"HOST": "custom.example.com", "CUSTOM-HEADER": "value"})
    req = make_request("get", "/test", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"
    assert req.headers["CUSTOM-HEADER"] == "value"

def test_make_request_invalid_method(make_request: _RequestMaker, app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/test")