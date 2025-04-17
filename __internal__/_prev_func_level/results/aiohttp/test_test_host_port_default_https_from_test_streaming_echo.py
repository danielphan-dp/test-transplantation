import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_port_default_http(make_request: _RequestMaker) -> None:
    req = make_request("get", "http://python.org/")
    assert req.host == "python.org"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'CUSTOM-HEADER': 'value'})
    req = make_request("get", "https://python.org/", headers=headers)
    assert req.headers['CUSTOM-HEADER'] == 'value'

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://python.org/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_host_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")

def test_host_missing_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "https://python.org/", headers=None)
    assert req.headers['HOST'] == 'server.example.com'
    assert req.headers['UPGRADE'] == 'websocket'