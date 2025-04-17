import pytest
from aiohttp import web
from multidict import CIMultiDict

@pytest.fixture
def app(loop: asyncio.AbstractEventLoop) -> web.Application:
    return web.Application()

@pytest.fixture
def protocol() -> web.RequestHandler[web.Request]:
    return mock.Mock()

def test_host_port_custom_headers(make_request: _RequestMaker) -> None:
    custom_headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket'})
    req = make_request("get", "wss://custom.example.com/", headers=custom_headers)
    assert req.host == "custom.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_port_no_headers(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://noheaders.example.com/")
    assert req.host == "noheaders.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_port_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://protocols.example.com/", protocols=True)
    assert req.host == "protocols.example.com"
    assert req.port == 443
    assert req.is_ssl()
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_host_port_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")