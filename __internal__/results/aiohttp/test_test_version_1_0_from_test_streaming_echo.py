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
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("GET", "/", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_make_request_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/")

def test_make_request_empty_path(make_request: _RequestMaker) -> None:
    req = make_request("GET", "")
    assert req.path == "/"  # Assuming the path defaults to root

def test_make_request_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", headers=None)
    assert req.headers['HOST'] == 'server.example.com'  # Check default headers are set

def test_make_request_with_version(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/", version="1.1")
    assert req.version == (1, 1)  # Check if version is set correctly

def test_make_request_with_invalid_version(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("GET", "/", version="invalid_version")