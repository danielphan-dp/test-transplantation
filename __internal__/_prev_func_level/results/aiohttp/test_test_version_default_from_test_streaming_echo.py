import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_make_request_default_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'
    assert req.headers['CONNECTION'] == 'Upgrade'
    assert req.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert req.headers['ORIGIN'] == 'http://example.com'
    assert req.headers['SEC-WEBSOCKET-VERSION'] == '13'

def test_make_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_make_request_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    req = make_request("GET", "/", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'custom_value'

def test_make_request_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/")

def test_make_request_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("GET", "")
    assert req.path == "/"  # Assuming empty path defaults to root

def test_make_request_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=None)
    assert req.headers['HOST'] == 'server.example.com'  # Default headers should be applied

def test_make_request_with_multiple_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HEADER1': 'value1', 'HEADER2': 'value2'})
    req = make_request("GET", "/", headers=custom_headers)
    assert req.headers['HEADER1'] == 'value1'
    assert req.headers['HEADER2'] == 'value2'