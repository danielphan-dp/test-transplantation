import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_path_is_double_encoded(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/test%20case%20again")
    assert req.url.raw_path == "/get/test%20case%20again"

def test_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "/test", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/test", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_request_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/test")
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/test")