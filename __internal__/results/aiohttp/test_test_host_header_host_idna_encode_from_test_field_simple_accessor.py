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
    req = make_request("get", "/")
    assert req.headers["HOST"] == "server.example.com"
    assert req.headers["UPGRADE"] == "websocket"
    assert req.headers["CONNECTION"] == "Upgrade"

def test_host_header_with_custom_host(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com'})
    req = make_request("get", "/", headers=custom_headers)
    assert req.headers["HOST"] == "custom.example.com"

def test_host_header_with_idna_encoded_host(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://xn--9caa.com")
    assert req.headers["HOST"] == "xn--9caa.com"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_header_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/")
    assert "HOST" in req.headers
    assert "UPGRADE" in req.headers
    assert "CONNECTION" in req.headers

def test_host_header_with_empty_headers(make_request: _RequestMaker) -> None:
    empty_headers = CIMultiDict({})
    req = make_request("get", "/", headers=empty_headers)
    assert req.headers["HOST"] == "server.example.com"  # Default should apply

def test_host_header_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/")