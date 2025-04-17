import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    ret: web.Application = mock.create_autospec(web.Application, spec_set=True)
    return ret

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    ret = mock.Mock()
    return ret

def test_skip_default_connection_header(make_request: _RequestMaker) -> None:
    req = make_request(
        "get", "http://python.org/", skip_auto_headers={istr("connection")}
    )
    assert "Connection" not in req.headers

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'X-Custom-Header': 'value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)
    assert req.headers['X-Custom-Header'] == 'value'

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)
    assert 'HOST' in req.headers
    assert 'UPGRADE' in req.headers
    assert 'CONNECTION' in req.headers

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("INVALID_METHOD", "http://python.org/")