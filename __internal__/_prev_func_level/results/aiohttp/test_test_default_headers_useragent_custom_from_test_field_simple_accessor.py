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

def test_default_headers_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", protocols=True
    )

    assert "SEC-WEBSOCKET-PROTOCOL" in req.headers
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_default_headers_without_protocols(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/"
    )

    assert "SEC-WEBSOCKET-PROTOCOL" not in req.headers

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {
        "user-agent": "my custom agent",
        "x-custom-header": "custom value"
    }
    req = make_request(
        "get", "http://python.org/", headers=custom_headers
    )

    assert "USER-Agent" in req.headers
    assert "my custom agent" == req.headers["User-Agent"]
    assert "x-custom-header" in req.headers
    assert "custom value" == req.headers["x-custom-header"]

def test_empty_headers(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", headers={}
    )

    assert "USER-Agent" not in req.headers
    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"