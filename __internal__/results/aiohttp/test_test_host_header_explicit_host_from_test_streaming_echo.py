import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_header_default(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert req.headers["SEC-WEBSOCKET-PROTOCOL"] == "chat, superchat"

def test_host_header_case_insensitivity(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={"host": "EXAMPLE.COM"})
    assert req.headers["HOST"] == "EXAMPLE.COM"

def test_host_header_missing(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={})
    assert req.headers["HOST"] == "server.example.com"

def test_host_header_multiple_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers={"host": "example.com", "HOST": "another.com"})
    assert req.headers["HOST"] == "another.com"