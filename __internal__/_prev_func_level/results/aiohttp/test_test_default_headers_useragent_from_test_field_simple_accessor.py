import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'custom_value'})
    req = make_request("get", "http://python.org/", headers=custom_headers)

    assert req.headers['CUSTOM-HEADER'] == 'custom_value'
    assert 'SERVER' not in req.headers
    assert 'USER-AGENT' in req.headers

def test_protocols_header(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", protocols=True)

    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/", headers=None)

    assert 'HOST' in req.headers
    assert 'UPGRADE' in req.headers
    assert 'CONNECTION' in req.headers
    assert 'SEC-WEBSOCKET-KEY' in req.headers
    assert 'ORIGIN' in req.headers
    assert 'SEC-WEBSOCKET-VERSION' in req.headers

def test_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org/")