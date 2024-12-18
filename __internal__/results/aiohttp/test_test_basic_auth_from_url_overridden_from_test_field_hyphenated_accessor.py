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
    req = make_request("GET", "/")
    assert "AUTHORIZATION" not in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert req.headers["UPGRADE"] == "websocket"
    assert req.headers["CONNECTION"] == "Upgrade"
    assert req.headers["SEC-WEBSOCKET-KEY"] == "dGhlIHNhbXBsZSBub25jZQ=="
    assert req.headers["ORIGIN"] == "http://example.com"
    assert req.headers["SEC-WEBSOCKET-VERSION"] == "13"

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({"CUSTOM-HEADER": "value"})
    req = make_request("POST", "/custom", headers=custom_headers)
    assert req.headers["CUSTOM-HEADER"] == "value"

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_make_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/")

def test_make_request_with_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("GET", "")
    assert req.path == "/"  # Assuming the default behavior is to treat empty path as root

def test_make_request_with_none_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=None)
    assert "AUTHORIZATION" not in req.headers
    assert req.headers["HOST"] == "server.example.com"  # Default headers should be applied

def test_make_request_with_auth(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://user:pass@python.org")
    assert "AUTHORIZATION" in req.headers
    assert req.headers["AUTHORIZATION"] == "Basic dXNlcjpwYXNz"
    assert req.host == "python.org"