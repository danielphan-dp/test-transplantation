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

def test_path_is_not_double_encoded2(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://0.0.0.0/get/test%20case%20with%20spaces")
    assert req.url.raw_path == "/get/test%20case%20with%20spaces"

def test_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "/path", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_request_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "/path", headers=None)
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "/path")