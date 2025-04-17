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
    req_with_headers = make_request("get", "http://python.org", headers=custom_headers)
    assert str(req_with_headers.url) == "http://python.org"
    assert req_with_headers.headers['CUSTOM-HEADER'] == 'value'

def test_params_with_protocols(make_request: _RequestMaker) -> None:
    req_with_protocols = make_request("get", "http://python.org", protocols=True)
    assert str(req_with_protocols.url) == "http://python.org"
    assert req_with_protocols.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_params_invalid_method(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("invalid_method", "http://python.org")

def test_params_empty_headers(make_request: _RequestMaker) -> None:
    req_empty_headers = make_request("get", "http://python.org", headers={})
    assert str(req_empty_headers.url) == "http://python.org"
    assert len(req_empty_headers.headers) == 0

def test_params_no_path(make_request: _RequestMaker) -> None:
    req_no_path = make_request("get", "")
    assert str(req_no_path.url) == "http://server.example.com/"
    assert req_no_path.method == "GET"