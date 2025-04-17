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

def test_host_port_default_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://example.com/")
    assert req.host == "example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_port_https_ws(make_request: _RequestMaker) -> None:
    req = make_request("get", "wss://secure.example.com/")
    assert req.host == "secure.example.com"
    assert req.port == 443
    assert req.is_ssl()

def test_host_with_custom_headers(make_request: _RequestMaker) -> None:
    headers = CIMultiDict({'HOST': 'custom.example.com', 'UPGRADE': 'websocket'})
    req = make_request("get", "ws://custom.example.com/", headers=headers)
    assert req.host == "custom.example.com"
    assert req.port == 80
    assert not req.is_ssl()

def test_host_with_protocols(make_request: _RequestMaker) -> None:
    req = make_request("get", "ws://example.com/", protocols=True)
    assert req.headers['SEC-WEBSOCKET-PROTOCOL'] == 'chat, superchat'

def test_host_invalid_url(make_request: _RequestMaker) -> None:
    with pytest.raises(ValueError):
        make_request("get", "invalid-url")