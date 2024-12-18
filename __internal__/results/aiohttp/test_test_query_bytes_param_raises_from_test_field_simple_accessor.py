import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_with_default_headers(make_request: _RequestMaker) -> None:
    request = make_request('GET', '/')
    assert request.headers['HOST'] == 'server.example.com'
    assert request.headers['UPGRADE'] == 'websocket'
    assert request.headers['CONNECTION'] == 'Upgrade'
    assert request.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert request.headers['ORIGIN'] == 'http://example.com'
    assert request.headers['SEC-WEBSOCKET-VERSION'] == '13'

def test_make_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    request = make_request('POST', '/test', headers=custom_headers)
    assert request.headers['CUSTOM-HEADER'] == 'custom_value'

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    request = make_request('GET', '/', protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request('INVALID_METHOD', '/')

def test_make_request_with_empty_path(make_request: _RequestMaker) -> None:
    request = make_request('GET', '')
    assert request.path == ''