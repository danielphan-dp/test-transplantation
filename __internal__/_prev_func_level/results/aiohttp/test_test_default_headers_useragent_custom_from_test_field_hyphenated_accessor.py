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

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = {
        "user-agent": "my custom agent",
        "x-custom-header": "custom value"
    }
    req = make_request("get", "http://python.org/", headers=custom_headers)

    assert "USER-Agent" in req.headers
    assert "my custom agent" == req.headers["User-Agent"]
    assert "X-Custom-Header" in req.headers
    assert "custom value" == req.headers["X-Custom-Header"]

def test_missing_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)

    assert "HOST" in req.headers
    assert req.headers["HOST"] == "server.example.com"
    assert "UPGRADE" in req.headers
    assert req.headers["UPGRADE"] == "websocket"