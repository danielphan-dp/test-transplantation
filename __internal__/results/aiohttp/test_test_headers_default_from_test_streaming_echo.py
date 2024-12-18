import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_headers_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", headers={"ACCEPT-ENCODING": "deflate"}, protocols=True
    )
    assert req.headers["ACCEPT-ENCODING"] == "deflate"
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_headers_without_protocols(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", headers={"ACCEPT-ENCODING": "gzip"}, protocols=False
    )
    assert req.headers["ACCEPT-ENCODING"] == "gzip"
    assert "SEC-WEBSOCKET-PROTOCOL" not in req.headers

def test_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.headers["HOST"] == "server.example.com"
    assert req.headers["UPGRADE"] == "websocket"
    assert req.headers["CONNECTION"] == "Upgrade"
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="
    assert req.headers["ORIGIN"] == "http://example.com"
    assert req.headers["SEC-WEBSOCKET-VERSION"] == "13"