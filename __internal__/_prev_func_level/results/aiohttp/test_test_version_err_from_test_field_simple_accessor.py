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

def test_make_request_default_headers(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    request = make_request(app, protocol)("GET", "/")
    assert request.headers['HOST'] == 'server.example.com'
    assert request.headers['UPGRADE'] == 'websocket'
    assert request.headers['CONNECTION'] == 'Upgrade'
    assert request.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert request.headers['ORIGIN'] == 'http://example.com'
    assert request.headers['SEC-WEBSOCKET-VERSION'] == '13'

def test_make_request_with_custom_headers(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    request = make_request(app, protocol)("GET", "/", headers=custom_headers)
    assert request.headers['CUSTOM-HEADER'] == 'custom_value'

def test_make_request_with_protocols(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    request = make_request(app, protocol)("GET", "/", protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_invalid_method(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    with pytest.raises(ValueError):
        make_request(app, protocol)("INVALID_METHOD", "/")

def test_make_request_empty_path(app: web.Application, protocol: web.RequestHandler[web.Request]) -> None:
    with pytest.raises(ValueError):
        make_request(app, protocol)("GET", "")