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

def test_path_not_contain_fragment2(make_request: _RequestMaker) -> None:
    req = make_request("GET", "http://example.com/path/to/resource#fragment")
    assert req.url.path == "/path/to/resource"

def test_request_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("GET", "/path", headers=custom_headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_request_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/path", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_request_without_headers(make_request: _RequestMaker) -> None:
    req = make_request("GET", "/path", headers=None)
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_request_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "/path")