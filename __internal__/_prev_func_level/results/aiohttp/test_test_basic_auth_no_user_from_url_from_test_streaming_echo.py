import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'CustomValue'})
    req = make_request("get", "/test", headers=custom_headers)
    assert "CUSTOM-HEADER" in req.headers
    assert req.headers["CUSTOM-HEADER"] == "CustomValue"

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/test", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/test")
    assert "AUTHORIZATION" in req.headers
    assert "Basic OjEyMzQ=" == req.headers["AUTHORIZATION"]
    assert "server.example.com" == req.host

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/test")

def test_make_request_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("get", "")
    assert req.path == "/"