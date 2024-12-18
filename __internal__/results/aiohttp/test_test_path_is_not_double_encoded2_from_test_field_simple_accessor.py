import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_with_default_headers(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    req = make_request(app, protocol)("GET", "/test")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['ORIGIN'] == 'http://example.com'
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'

def test_make_request_with_custom_headers(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    req = make_request(app, protocol)("POST", "/test", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'custom_value'

def test_make_request_with_protocols(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    req = make_request(app, protocol)("GET", "/test", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_with_invalid_method(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    with pytest.raises(ValueError):
        make_request(app, protocol)("INVALID_METHOD", "/test")

def test_make_request_with_empty_path(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    req = make_request(app, protocol)("GET", "")
    assert req.url.raw_path == "/"