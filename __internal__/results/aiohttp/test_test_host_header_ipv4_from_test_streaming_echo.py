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
    req = make_request("get", "http://server.example.com")
    assert req.headers["HOST"] == "server.example.com"
    assert req.headers["UPGRADE"] == "websocket"
    assert req.headers["CONNECTION"] == "Upgrade"
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="
    assert req.headers["ORIGIN"] == "http://example.com"
    assert req.headers["SEC-WEBSOCKET-VERSION"] == "13"

def test_host_header_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket'})
    req = make_request("get", "http://custom.example.com", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"
    assert req.headers["UPGRADE"] == "websocket"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://server.example.com", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_header_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://server.example.com")

def test_host_header_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    assert req.path == ""