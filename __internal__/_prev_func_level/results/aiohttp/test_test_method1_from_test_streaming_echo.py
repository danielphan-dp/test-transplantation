import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_get_method(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/")
    assert req.method == "GET"

def test_make_request_post_method(make_request: _RequestMaker) -> None:
    req = make_request("POST", "/submit")
    assert req.method == "POST"

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'Authorization': 'Bearer token'})
    req = make_request("GET", "/secure", headers=headers)
    assert req.headers['Authorization'] == 'Bearer token'

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['ORIGIN'] == 'http://example.com'
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'