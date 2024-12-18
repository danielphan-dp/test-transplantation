import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return mock.create_autospec(web.Application, spec_set=True)

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    ret.set_parser.return_value = ret
    return ret

def test_make_request_with_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com")
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert "UPGRADE" in req.headers
    assert req.headers["UPGRADE"] == "websocket"
    assert "SEC-WEBSOCKET-KEY" in req.headers
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({"CUSTOM-HEADER": "custom_value"})
    req = make_request("get", "http://example.com", headers=custom_headers)
    assert "CUSTOM-HEADER" in req.headers
    assert req.headers["CUSTOM-HEADER"] == "custom_value"

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://example.com", protocols=True)
    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://example.com")