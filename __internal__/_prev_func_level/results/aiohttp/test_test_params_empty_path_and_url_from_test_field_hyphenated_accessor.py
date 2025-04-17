import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_params_with_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req_with_custom_headers = make_request("get", "http://python.org", headers=custom_headers)
    assert req_with_custom_headers.headers['CUSTOM-HEADER'] == 'value'

def test_params_with_protocols(make_request: _RequestMaker) -> None:
    req_with_protocols = make_request("get", "http://python.org", protocols=True)
    assert req_with_protocols.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_params_with_empty_headers(make_request: _RequestMaker) -> None:
    req_empty_headers = make_request("get", "http://python.org", headers=CIMultiDict())
    assert 'HOST' in req_empty_headers.headers
    assert req_empty_headers.headers['HOST'] == 'server.example.com'

def test_params_with_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org")

def test_params_with_none_headers(make_request: _RequestMaker) -> None:
    req_none_headers = make_request("get", "http://python.org", headers=None)
    assert 'HOST' in req_none_headers.headers
    assert req_none_headers.headers['HOST'] == 'server.example.com'