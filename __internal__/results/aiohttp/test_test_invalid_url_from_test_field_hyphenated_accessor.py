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

def test_missing_headers(make_request: _RequestMaker) -> None:
    request = make_request("get", "/")
    assert request.headers['HOST'] == 'server.example.com'
    assert request.headers['UPGRADE'] == 'websocket'
    assert request.headers['CONNECTION'] == 'Upgrade'
    assert request.headers['SEC-WEBSOCKET-KEY'] == 'dGhlIHNhbXBsZSBub25jZQ=='
    assert request.headers['ORIGIN'] == 'http://example.com'
    assert request.headers['SEC-WEBSOCKET-VERSION'] == '13'

def test_with_protocols(make_request: _RequestMaker) -> None:
    request = make_request("get", "/", protocols=True)
    assert request.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(aiohttp.InvalidMethod):
        make_request("invalid_method", "/")

def test_empty_path(make_request: _RequestMaker) -> None:
    with pytest.raises(aiohttp.InvalidURL):
        make_request("get", "")

def test_invalid_header_format(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'Invalid-Header': 'value'})
    request = make_request("get", "/", headers=headers)
    assert request.headers['Invalid-Header'] == 'value'