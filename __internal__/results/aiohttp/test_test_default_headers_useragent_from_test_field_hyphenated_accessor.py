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

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)

    assert req.headers['CUSTOM-HEADER'] == 'value'
    assert "SERVER" not in req.headers
    assert "USER-AGENT" in req.headers

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)

    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)

    assert "SERVER" not in req.headers
    assert "USER-AGENT" in req.headers
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org/")